import json
from web3.middleware import geth_poa_middleware
from web3 import Web3, HTTPProvider
from time import sleep
from itertools import islice
from events import fetch_events

'''
RESET INSTRUCTIONS:
Put 0 to last_block_number.json and then run to filter the blocks from begining of the contract
'''

# Switch Mainnet/Testnet
CHAINID = 5  # 1 for Ethereum mainnet & 5 for Goerli testnet
TESTURL = "https://eth-goerli.g.alchemy.com/v2/surwT5Ql_QhEc083ru_C98XrwbDj-jVx"
with open("abi.json") as f:
    info_json = json.load(f)
ABI = info_json
CONTRACT_ADDRESS = "0x60F2CE0a06E1974a1378322B948567673f6eBF89"

# Script Wallet Address Details
PRIVKEY = "4349749f97226605564c20fa6b9f35f259456a710ce23ca01bffe239cab3ae5f"
WALLETADDRESS = "0x04c63D8c2fc9DD602aeE46F12083af1DdE69C713"

# Initializing web3
w3 = Web3(Web3.HTTPProvider(TESTURL))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
# Returns true if connected successfully to the network otherwise false
print(w3.isConnected())

# Initializing Contract
CONTRACT = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
LAST_BLOCK_FILE = open('last_block_number.json', 'r')
LAST_BLOCK = int(LAST_BLOCK_FILE.read())
LAST_BLOCK_FILE.close()

def fill_Dict(ev, dic):
    try:
        # If the address is already in the dict just add the nos of tokens
        dic[ev.args.to] = dic[ev.args.to] + \
            ev.args.value
    except KeyError:
        dic[ev.args.to] = ev.args.value

def sort_Dict(dic):
    return dict(sorted(dic.items(), key=lambda item: item[1]))

def filter_elements(n, iterable):
    "Return first n items of the iterable as a list"
    return list(reversed(list(islice(iterable, n))))

def fetch_my_events(CONTRACT, LAST_BLOCK, DICT):

    events = list(fetch_events(
        CONTRACT.events.Transfer, from_block=LAST_BLOCK))

    print(len(events))

    inner_lst_blk = LAST_BLOCK

    # Checking event if its not 0 then update the LAST BLOCK NUMBER
    if(len(events) is not 0):

        for ev in events:
            # Filling up the dict with wallet address and nos of tokens
            fill_Dict(ev, DICT)
            inner_lst_blk = ev.blockNumber
    
        # Sort them
        DICT = sort_Dict(DICT)

        # Represent max. 25 wallets from the list
        final_ELES = filter_elements(25, DICT.items())
        for key, value in final_ELES:
            print(key, w3.fromWei(value, "ether"))

    return inner_lst_blk


while True:
    LAST_BLOCK = fetch_my_events(CONTRACT, LAST_BLOCK, {}) + 1
    with open('last_block_number.json', 'w') as block_file:    
        block_file.write(str(LAST_BLOCK))
        block_file.close()
    sleep(21600) # awaiting for 6 hours
