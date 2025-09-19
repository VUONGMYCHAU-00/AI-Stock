from web3 import Web3
from solcx import compile_standard, install_solc
import json
import os

# RPC URL from Ganache
RPC = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(RPC))
assert w3.is_connected(), "Cannot connect to Ganache. Start Ganache first."

# account (Ganache provides unlocked accounts)
acct = w3.eth.accounts[0]

# read solidity
with open("blockchain/Log.sol", "r") as f:
    source = f.read()

# install solc if needed
install_solc("0.8.17")

compiled = compile_standard({
    "language": "Solidity",
    "sources": {"Log.sol": {"content": source}},
    "settings": {"outputSelection": {"*": {"*": ["abi","metadata","evm.bytecode"]}}}
}, solc_version="0.8.17")

bytecode = compiled['contracts']['Log.sol']['LogStorage']['evm']['bytecode']['object']
abi = compiled['contracts']['Log.sol']['LogStorage']['abi']

Log = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = Log.constructor().transact({'from': acct})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Contract deployed at:", tx_receipt.contractAddress)

# save ABI + address
os.makedirs("blockchain/artifacts", exist_ok=True)
with open("blockchain/artifacts/abi.json", "w") as f:
    json.dump(abi, f)
with open("blockchain/artifacts/address.txt", "w") as f:
    f.write(tx_receipt.contractAddress)
print("ABI and address saved to blockchain/artifacts/")
