import json
import random
from web3.middleware import geth_poa_middleware
from web3 import Web3, HTTPProvider
from time import sleep

'''
Instructions to run:
Change your wallet address and PRIVKEY

###pip install web3

Run on Terminal:
###python TransactionScript.py

Check that you haev enpough gas fee for the transactions + SJT tokens
'''

# Switch Mainnet/Testnet
CHAINID = 5  # 1 for Ethereum mainnet & 5 for Goerli testnet
TESTURL = "https://eth-goerli.g.alchemy.com/v2/surwT5Ql_QhEc083ru_C98XrwbDj-jVx"

# Wallet Address Details
PRIVKEY = "4349749f97226605564c20fa6b9f35f259456a710ce23ca01bffe239cab3ae5f" # Private key of your wallet
WALLETADDRESS = "0x04c63D8c2fc9DD602aeE46F12083af1DdE69C713" # Address of your wallet (SJT + GAS fee should be their)

# Below where the receivers are :)
WalletAddresses = ['0x2caF424F1BcbEf1f1D7dF082c6b5677f0283f9d7',
                   '0xC5EE6df742d1Ec2D0C7fFA93CFCb92eaE1eFE865', '0x9C96a2B3FB3871e6CE4ea6587801F89D2a6094e1', '0x990c8121ec42C9b7a3049Df585352759c2eA149e', '0x44492C089a11D4d60B8D0EB3f8eC0EFA14F88f6b']

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


while True:
    for i in WalletAddresses:
        # Building Transaction
        transaction = contract.functions.transfer(i, random.randint(10, 90)*1000000000000000000).buildTransaction({"from": WALLETADDRESS,
                                                                                                        "chainId": CHAINID,
                                                                                                        "nonce": w3.eth.get_transaction_count(WALLETADDRESS)
                                                                                                        })
        # Signing Transaction Using PRIVKEY
        signed_txn = w3.eth.account.signTransaction(
            transaction, PRIVKEY)
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(txn_hash.hex())
        sleep(60)
    sleep(60)
    # To Exit: CTRL + C
