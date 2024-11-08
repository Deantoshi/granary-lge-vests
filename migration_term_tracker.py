import pandas as pd
from web3 import Web3
from web3.middleware import geth_poa_middleware 
import time

WAIT_TIME = 0.75

# # makes our web3 object and injects it's middleware
def get_web_3(rpc_url):

    if 'wss' in rpc_url:
        provider = Web3.WebsocketProvider(rpc_url)
        web3 = Web3(provider)
    else:
        web3 = Web3(Web3.HTTPProvider(rpc_url))
    time.sleep(1)
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    time.sleep(1)
    
    return web3

# # finds the latest block on a given blockchain
def get_latest_block(web3):

    latest_block = web3.eth.get_block_number()

    return latest_block

# # gets the migration abi
def get_abi():

    abi = [{"inputs":[{"internalType":"address","name":"_initalOwner","type":"address"},{"internalType":"uint256","name":"_deadline","type":"uint256"},{"internalType":"contract IERC20","name":"_oath","type":"address"},{"internalType":"contract IERC20","name":"_grain","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"target","type":"address"}],"name":"AddressEmptyCode","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"AddressInsufficientBalance","type":"error"},{"inputs":[],"name":"FailedInnerCall","type":"error"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"OwnableInvalidOwner","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"OwnableUnauthorizedAccount","type":"error"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"SafeERC20FailedOperation","type":"error"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"DeadlineUpdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"sender","type":"address"},{"indexed":False,"internalType":"uint256","name":"amountOATH","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"amountGRAIN","type":"uint256"},{"indexed":False,"internalType":"bool","name":"vest","type":"bool"}],"name":"Deposit","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"inputs":[],"name":"deadline","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amountOATH","type":"uint256"},{"internalType":"uint256","name":"_amountGRAIN","type":"uint256"},{"internalType":"bool","name":"_requestVest","type":"bool"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_deadline","type":"uint256"}],"name":"extendDeadline","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"grain","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"oath","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"_token","type":"address"},{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"rescueTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"terms","outputs":[{"internalType":"uint256","name":"amountOATH","type":"uint256"},{"internalType":"uint256","name":"amountGRAIN","type":"uint256"},{"internalType":"bool","name":"vest","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]

    return abi

# # gets the web3 contract object
def get_contract(contract_address, rpc_url, web3):
        
        abi = get_abi()

        web3 = get_web_3(rpc_url)

        contract = web3.eth.contract(address=contract_address, abi=abi)

        time.sleep(WAIT_TIME)

        return contract

# # takes in a contract object and returns all associated deposit events
def get_deposit_events(contract, from_block, to_block):

    # events = contract.events.Transfer.get_logs(fromBlock=from_block, toBlock=latest_block)
    events = contract.events.Deposit.get_logs(fromBlock=from_block, toBlock=to_block)

    return events

# # makes a dataframe out of our deposit events
def process_events(events, chain, web3):

    df = pd.DataFrame()

    send_address_list = []
    oath_amount_list = []
    grain_amount_list = []
    vest_list = []
    tx_hash_list = []
    timestamp_list = []
    block_list = []

    for event in events:

        send_address = event['args']['sender']
        oath_amount = event['args']['amountOATH']
        grain_amount = event['args']['amountGRAIN']
        vest = event['args']['vest']


        tx_hash = event['transactionHash'].hex()

        try:
            block = web3.eth.get_block(event['blockNumber'])
            block_number = int(block['number'])
            time.sleep(WAIT_TIME)
        except:
            block_number = int(event['blockNumber'])
        
        try:
            block_timestamp = block['timestamp']
        except:
            block_timestamp = 1776

        # # Here **
        
        # # handles stuff if there are multiple senders
        # if len(send_address) > 1:
        #     i = 0

        #     while i < len(send_address):
        #         print(event)
        #         send_address = send_address[i]
        #         oath_amount = oath_amount[i]
        #         grain_amount = grain_amount[i]
        #         vest = vest[i]
        #         tx_hash = tx_hash[i]
        #         block_number = block_number[i]
        #         block_timestamp = block_timestamp[i]


        #         send_address_list.append(send_address)
        #         oath_amount_list.append(oath_amount)
        #         grain_amount_list.append(grain_amount)
        #         vest_list.append(vest)
        #         tx_hash_list.append(tx_hash)
        #         block_list.append(block_number)
        #         timestamp_list.append(block_timestamp)
            
        #     i += 1

        send_address_list.append(send_address)
        oath_amount_list.append(oath_amount)
        grain_amount_list.append(grain_amount)
        vest_list.append(vest)
        tx_hash_list.append(tx_hash)
        block_list.append(block_number)
        timestamp_list.append(block_timestamp)


    if len(send_address_list) > 0:
        df['sender_address'] = send_address_list
        df['oath_amount'] = oath_amount_list
        df['grain_amount'] = grain_amount_list
        df['vest'] = vest_list
        df['tx_hash'] = tx_hash_list
        df['blocknumber'] = block_list
        df['timestamp'] = timestamp_list
        df['chain'] = chain
     
    return df

# # loops through all of our migration contracts
def run_all():
     
    rpc_list = ['https://optimism.llamarpc.com', 'https://rpc.ftm.tools', 'https://andromeda.metis.io/?owner=1088']
    migration_contract_list = ['0x2B335F56FbF878BB3516110E5bc342eC5Db66F87', '0xd3dC4851543f7306225A9aBaB2c68e1f28ab0202', '0x4BFfD3564Cf3DD9e68c1de3F4a1E00d023a0E378']
    chain_list = ['OP', 'FTM', 'METIS']
    from_block_list = [122695367, 87364739, 17666256]
    interval = 5000

    df = pd.DataFrame()

    i = 0

    df_list = []

    # # loops through each contract
    while i < len(rpc_list):
        rpc_url = rpc_list[i]
        migration_contract_address = migration_contract_list[i]
        chain = chain_list[i]
        from_block = from_block_list[i]

        to_block = from_block + interval
        
        web3 = get_web_3(rpc_url)

        contract = get_contract(migration_contract_address, rpc_url, web3)

        latest_block = get_latest_block(web3)
        
        # # loops through a specific's contract event history
        while to_block < latest_block:
             
            events = get_deposit_events(contract, from_block, to_block)

            if len(events) > 0:
                df = process_events(events, chain, web3)
            
            if len(df) > 0:
                print(df)

                df_list.append(df)
            
            time.sleep(WAIT_TIME)

            from_block += interval
            to_block += interval

            # print(deposit_events)

            df = pd.DataFrame()

            if from_block >= latest_block:
                from_block = latest_block - 1
            
            if to_block >= latest_block:
                to_block = latest_block

            print(chain, ' Current Event Block vs Latest Event Block to Check: ', from_block, '/', latest_block, 'Blocks Remaining: ', latest_block - from_block)

        i += 1

    df = pd.concat(df_list)

    return df

# # returns how much grain there is to be claimed
def get_terms(contract, wallet_address, chain):

    df = pd.DataFrame()

    user_data = contract.functions.terms(wallet_address).call()

    amount_oath = user_data[0]
    amount_grain = user_data[1]
    vest = user_data[2]

    df['wallet_address'] = [wallet_address]
    df['amount_oath'] = [amount_oath]
    df['amount_grain'] = [amount_grain]
    df['vest'] = [vest]
    df['chain'] = [chain]

    return df

def run_all_migration_terms():
    
    rpc_list = ['https://optimism.llamarpc.com', 'https://rpc.ftm.tools', 'https://andromeda.metis.io/?owner=1088']
    migration_contract_list = ['0x2B335F56FbF878BB3516110E5bc342eC5Db66F87', '0xd3dC4851543f7306225A9aBaB2c68e1f28ab0202', '0x4BFfD3564Cf3DD9e68c1de3F4a1E00d023a0E378']
    chain_list = ['OP', 'FTM', 'METIS']
    from_block_list = [122695367, 87364739, 17666256]
    interval = 5000

    df = pd.read_csv('test_test.csv')

    i = 0

    df_list = []

    # # loops through each contract
    while i < len(rpc_list):
        rpc_url = rpc_list[i]
        migration_contract_address = migration_contract_list[i]
        chain = chain_list[i]
        
        web3 = get_web_3(rpc_url)

        contract = get_contract(migration_contract_address, rpc_url, web3)

        chain_df = df.loc[df['chain'] == chain]

        unique_chain_user_list = chain_df['sender_address'].unique()

        user_count = 0
        for unique_chain_user in unique_chain_user_list:
            user_term_df = get_terms(contract, unique_chain_user, chain)
            time.sleep(WAIT_TIME)

            if len(user_term_df) > 0:
                df_list.append(user_term_df)
                # print(user_term_df)
                # print(df_list)
            
            print(chain, 'Wallets Remaining: ', user_count, '/', len(unique_chain_user_list), 'Count Remaining: ', len(unique_chain_user_list) - user_count)
            
            user_count += 1

        i += 1

    df = pd.concat(df_list)
    df = df.drop_duplicates(subset=['wallet_address', 'amount_oath', 'amount_grain', 'vest', 'chain'])

    return df

# df = run_all()

# df.to_csv('test_test.csv', index=False)

df = run_all_migration_terms()

df.to_csv('user_cdx_terms.csv', index=False)