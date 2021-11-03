
from solcx import compile_standard
import json
from web3 import Web3
import os

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Compile solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources":  {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metada", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


# Get the bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# Get the abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connecting to ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x91cc3168351da6B80fC1aD209aa6b9B87718832F"
private_key = "0x571ae5b5cb03f99b1295ad7c9f2d55ff62676ca1f0c6aa610b3b0ac56b8b32c0"

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
# 1. Build a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce})

# 2. Sign
signed_transaction = w3.eth.account.sign_transaction(
    transaction, private_key=private_key)

# 3. Send
transaction_hash = w3.eth.send_raw_transaction(
    signed_transaction.rawTransaction)
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

# Working with the contract
# Contract Address
# Contract ABI
simple_storage = w3.eth.contract(
    address=transaction_receipt.contractAddress, abi=abi)
print(simple_storage.functions.retreive().call())

store_transaction = simple_storage.functions.store(15).buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce+1}
)
signed_store_tx = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key)
transaction_hash = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

print(simple_storage.functions.retreive().call())
