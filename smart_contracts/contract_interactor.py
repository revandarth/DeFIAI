from web3 import Web3
from dotenv import load_dotenv
import os
import json

load_dotenv()

class ContractInteractor:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(os.getenv('ETHEREUM_NODE_URL')))
        self.account = self.w3.eth.account.from_key(os.getenv('PRIVATE_KEY'))
        
        with open('smart_contracts/build/contracts/TradingExecutor.json') as f:
            contract_json = json.load(f)
        self.contract = self.w3.eth.contract(
            address=os.getenv('CONTRACT_ADDRESS'),
            abi=contract_json['abi']
        )

    def request_prediction(self):
        tx = self.contract.functions.requestPricePrediction().build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
        })
        signed_tx = self.account.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return self.w3.eth.wait_for_transaction_receipt(tx_hash)

    def get_latest_price(self):
        return self.contract.functions.latestPrice().call()

# Usage example
if __name__ == "__main__":
    interactor = ContractInteractor()
    interactor.request_prediction()
    print(f"Latest price prediction: {interactor.get_latest_price()}")