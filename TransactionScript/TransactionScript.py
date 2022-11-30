import json, random
from web3.middleware import geth_poa_middleware
from web3 import Web3, HTTPProvider
from time import sleep

'''
Instructions to run:
###pip install web3

Run on Terminal:
###python TransactionScript.py
'''

# Switch Mainnet/Testnet
CHAINID = 5  # 1 for Ethereum mainnet & 5 for Goerli testnet
TESTURL = "https://eth-goerli.g.alchemy.com/v2/surwT5Ql_QhEc083ru_C98XrwbDj-jVx"

# Wallet Address Details
PRIVKEY = "4349749f97226605564c20fa6b9f35f259456a710ce23ca01bffe239cab3ae5f"
WALLETADDRESS = "0x04c63D8c2fc9DD602aeE46F12083af1DdE69C713"

WalletAddresses = ['0x38948Bcdc7cb074D61F38607d89F4c0d78907De5']

# Initializing web3
w3 = Web3(Web3.HTTPProvider(TESTURL))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
# Returns true if connected successfully to the network otherwise false
print(w3.isConnected())

# On Contract Change
CONTRACT_ADDRESS = "0x60F2CE0a06E1974a1378322B948567673f6eBF89"
with open("abi.json") as f:
    info_json = json.load(f)
ABI = info_json
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

def build_Trans(address, randInt):
    # Building Transaction
    transaction = contract.functions.transfer(address, randInt*1000000000000000000).buildTransaction({"from": WALLETADDRESS,
                                                              "chainId": CHAINID,
                                                              "nonce": w3.eth.getTransactionCount(WALLETADDRESS)
                                                              })

    # Signing Transaction Using PRIVKEY
    signed_txn = w3.eth.account.signTransaction(
        transaction, PRIVKEY)

    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # Returning the transaction HASH
    return txn_hash.hex()


while True:
    for i in WalletAddresses:
        print(build_Trans(i, random.randint(1,9)))
    sleep(60)
    # To Exit: CTRL + C