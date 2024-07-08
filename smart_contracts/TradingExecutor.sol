// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@uniswap/v2-periphery/contracts/interfaces/IUniswapV2Router02.sol";
import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";

contract TradingExecutor is ChainlinkClient {
 using Chainlink for Chainlink.Request;

 address public owner;
 IUniswapV2Router02 public uniswapRouter;
 IERC20 public tradingToken;
 address public constant WETH = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;

 uint256 public latestPrice;
 bytes32 private jobId;
 uint256 private fee;

 event PricePredictionReceived(uint256 price);
 event TradeExecuted(uint256 amount, uint256 received);

 constructor(address _router, address _tradingToken) {
     owner = msg.sender;
     uniswapRouter = IUniswapV2Router02(_router);
     tradingToken = IERC20(_tradingToken);

     setPublicChainlinkToken();
     jobId = "<chainlink_job_i>d"; // Yet to get these details
     fee = 0.1 * 10 ** 18; // 0.1 LINK
 }

 function requestPricePrediction() public {
     Chainlink.Request memory req = buildChainlinkRequest(jobId, address(this), this.fulfill.selector);
     req.add("get", "http://api-endpoint.com/predict"); // Need to generate them - in progress
     req.add("path", "price");
     sendChainlinkRequestTo(chainlinkOracleAddress(), req, fee);
 }

 function fulfill(bytes32 _requestId, uint256 _price) public recordChainlinkFulfillment(_requestId) {
     latestPrice = _price;
     emit PricePredictionReceived(_price);
     executeTrade();
 }

 function executeTrade() internal {
     uint256 balance = tradingToken.balanceOf(address(this));
     require(balance > 0, "No tokens to trade");

     tradingToken.approve(address(uniswapRouter), balance);

     address[] memory path = new address[](2);
     path[0] = address(tradingToken);
     path[1] = WETH;

     uint256[] memory amounts = uniswapRouter.swapExactTokensForETH(
         balance,
         0,
         path,
         address(this),
         block.timestamp + 15 minutes
     );

     emit TradeExecuted(balance, amounts[1]);
 }

 receive() external payable {}

 function withdraw() public {
     require(msg.sender == owner, "Only owner can withdraw");
     payable(owner).transfer(address(this).balance);
 }
}
