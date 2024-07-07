const TradingExecutor = artifacts.require("TradingExecutor");

module.exports = function(deployer, network) {
  let uniswapRouterAddress;
  let tradingTokenAddress;

  if (network === 'mainnet') {
    uniswapRouterAddress = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D';
    tradingTokenAddress = '0x6B175474E89094C44Da98b954EedeAC495271d0F'; // DAI address
  } else {
    // Use testnet addresses here
    uniswapRouterAddress = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D';
    tradingTokenAddress = '0x4F96Fe3b7A6Cf9725f59d353F723c1bDb64CA6Aa'; // Kovan DAI address
  }

  deployer.deploy(TradingExecutor, uniswapRouterAddress, tradingTokenAddress);
};