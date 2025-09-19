import json
from web3 import Web3
import os

RPC = "http://127.0.0.1:7545"  # Ganache
w3 = Web3(Web3.HTTPProvider(RPC))
if not w3.is_connected():
    raise Exception("Cannot connect to Ganache. Start Ganache.")

# load artifacts
ABI_PATH = "blockchain/artifacts/abi.json"
ADDR_PATH = "blockchain/artifacts/address.txt"
if not (os.path.exists(ABI_PATH) and os.path.exists(ADDR_PATH)):
    raise Exception("ABI or contract address not found. Deploy contract first.")

with open(ABI_PATH) as f:
    abi = json.load(f)
with open(ADDR_PATH) as f:
    address = f.read().strip()

contract = w3.eth.contract(address=address, abi=abi)
account = w3.eth.accounts[0]  # Ganache unlocked account

def save_log(log_type: str, data: str):
    # send transaction
    tx = contract.functions.addLog(log_type, data).transact({'from': account})
    receipt = w3.eth.wait_for_transaction_receipt(tx)
    return receipt.transactionHash.hex()

def get_all_logs():
    count = contract.functions.getLogCount().call()
    logs = []
    for i in range(count):
        logType, data, ts = contract.functions.getLog(i).call()
        logs.append({"id": i, "type": logType, "data": data, "timestamp": ts})
    return logs
