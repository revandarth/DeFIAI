# Smart Contract Integration

This module focuses on integrating our price prediction model with a smart contract for automated trading on Ethereum-based decentralized exchanges.

## Setup

1. Install required libraries:

```pip install web3 python-dotenv
```

### Install Truffle globally
```
npm install -g truffle

mkdir smart_contracts
cd smart_contracts
truffle init
```

### This smart contract does the following:

- Uses Chainlink to request price predictions from our off-chain model
- Receives the price prediction through a callback function
- Executes a trade on Uniswap based on the prediction
- Create a Python script to interact with the smart contract:


## Deployment

```npm install @openzeppelin/contracts

truffle migrate --network mainnet
```




