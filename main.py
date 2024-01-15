from flask import Flask, request, jsonify
from web3 import Web3
from web3.middleware import geth_poa_middleware
import pandas as pd
import json
from functools import cache
import threading 
import queue
import time
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# Replace with the actual Optimism RPC URL
optimism_rpc_url = 'https://eon-rpc.horizenlabs.io/ethv1'

# Create a Web3 instance to connect to the Optimism blockchain
web3 = Web3(Web3.HTTPProvider(optimism_rpc_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

LATEST_BLOCK = web3.eth.get_block_number()
FROM_BLOCK = 774589 - 1000
# FROM_BLOCK = 0

# Replace with the actual Aave V2 contract address
# contract_address = "0x871AfF0013bE6218B61b28b274a6F53DB131795F"


#gets how many decimals our reserve is
def get_reserve_decimals(reserve_address):
    decimals = 0
    if reserve_address == '0x38C2a6953F86a7453622B1E7103b738239728754': # dai
        decimals = 1e18
    elif reserve_address == '0xCc44eB064CD32AAfEEb2ebb2a47bE0B882383b53': # usdc
        decimals = 1e6
    elif reserve_address == '0xA167bcAb6791304EDa9B636C8beEC75b3D2829E6': # usdt
        decimals = 1e6
    elif reserve_address == '0x2c2E0B0c643aB9ad03adBe9140627A645E99E054': # weth
        decimals = 1e18
    elif reserve_address == '0x1d7fb99AED3C365B4DEf061B7978CE5055Dfc1e7': # wbtc
        decimals = 1e8
    
    return decimals
#gets our reserve price
#@cache
# def get_tx_usd_amount(reserve_address, token_amount):
#     contract_address = '0x8429d0AFade80498EAdb9919E41437A14d45A00B'
#     contract_abi = [{"inputs":[{"internalType":"address[]","name":"assets","type":"address[]"},{"internalType":"address[]","name":"sources","type":"address[]"},{"internalType":"address","name":"fallbackOracle","type":"address"},{"internalType":"address","name":"baseCurrency","type":"address"},{"internalType":"uint256","name":"baseCurrencyUnit","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"asset","type":"address"},{"indexed":True,"internalType":"address","name":"source","type":"address"}],"name":"AssetSourceUpdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"baseCurrency","type":"address"},{"indexed":False,"internalType":"uint256","name":"baseCurrencyUnit","type":"uint256"}],"name":"BaseCurrencySet","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"fallbackOracle","type":"address"}],"name":"FallbackOracleUpdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"inputs":[],"name":"BASE_CURRENCY","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"BASE_CURRENCY_UNIT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"}],"name":"getAssetPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"assets","type":"address[]"}],"name":"getAssetsPrices","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getFallbackOracle","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"}],"name":"getSourceOfAsset","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"assets","type":"address[]"},{"internalType":"address[]","name":"sources","type":"address[]"}],"name":"setAssetSources","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"fallbackOracle","type":"address"}],"name":"setFallbackOracle","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]
#     contract = web3.eth.contract(address=contract_address, abi=contract_abi)
#     value_usd = contract.functions.getAssetPrice(reserve_address).call()
#     decimals = get_reserve_decimals(reserve_address)
#     usd_amount = (value_usd/1e18)*(token_amount/decimals)
#     # print(usd_amount)
#     return usd_amount

#gets our web3 contract object
# @cache
def get_contract():
    contract_address = "0x0fdbD7BAB654B5444c96FCc4956B8DF9CcC508bE"
    contract_abi = [{"type":"constructor","stateMutability":"nonpayable","inputs":[{"type":"address","name":"weth","internalType":"address"},{"type":"address","name":"provider","internalType":"address"}]},{"type":"event","name":"OwnershipTransferred","inputs":[{"type":"address","name":"previousOwner","internalType":"address","indexed":True},{"type":"address","name":"newOwner","internalType":"address","indexed":True}],"anonymous":False},{"type":"fallback","stateMutability":"payable"},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"authorizeLendingPool","inputs":[{"type":"address","name":"lendingPool","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"borrowETH","inputs":[{"type":"address","name":"lendingPool","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"},{"type":"uint256","name":"interesRateMode","internalType":"uint256"},{"type":"uint16","name":"referralCode","internalType":"uint16"}]},{"type":"function","stateMutability":"payable","outputs":[],"name":"depositETH","inputs":[{"type":"address","name":"lendingPool","internalType":"address"},{"type":"address","name":"onBehalfOf","internalType":"address"},{"type":"uint16","name":"referralCode","internalType":"uint16"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"emergencyEtherTransfer","inputs":[{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"emergencyTokenTransfer","inputs":[{"type":"address","name":"token","internalType":"address"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"getSignature","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"getWETHAddress","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"owner","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"renounceOwnership","inputs":[]},{"type":"function","stateMutability":"payable","outputs":[],"name":"repayETH","inputs":[{"type":"address","name":"lendingPool","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"},{"type":"uint256","name":"rateMode","internalType":"uint256"},{"type":"address","name":"onBehalfOf","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"setSignature","inputs":[{"type":"string","name":"signature","internalType":"string"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"transferOwnership","inputs":[{"type":"address","name":"newOwner","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"withdrawETH","inputs":[{"type":"address","name":"lendingPool","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"}]},{"type":"receive","stateMutability":"payable"}]
    
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    return contract

# gets the last block number we have gotten data from and returns this block number
def get_last_block_tracked():
    df = pd.read_csv('all_users.csv')
    
    last_block_monitored = df['last_block_number'].max()

    last_block_monitored = int(last_block_monitored)

    return last_block_monitored

print(get_last_block_tracked())

#makes a dataframe and stores it in a csv file
def make_user_data_csv(df):
    old_df = pd.read_csv('all_users.csv')
    old_df = old_df.drop_duplicates(subset=['wallet_address','tx_hash','number_of_tokens','block_number'], keep='last')

    combined_df_list = [df, old_df]

    combined_df = pd.concat(combined_df_list)
    combined_df = combined_df.drop_duplicates(subset=['wallet_address','tx_hash','number_of_tokens','block_number'], keep='last')

    # combined_df['txHash'] = combined_df['txHash'].str.lower()
    # combined_df['tokenAddress'] = combined_df['tokenAddress'].str.lower()

    # print(df)
    # print(len(old_df), len(df), len(combined_df))

    if len(combined_df) >= len(old_df):
        combined_df['last_block_number'] = int(df['last_block_number'].max())
        combined_df.to_csv('all_users.csv', index=False)
        print('CSV Made')

    elif len(combined_df) > 0:
        combined_df['last_block_number'] = int(df['last_block_number'].max())
        combined_df.to_csv('all_users.csv', index=False)
        print('CSV Made')
    
    return

# Gets transactions of all blocks within a specified range and returns a df with info from blocks that include our contract
def get_all_gateway_transactions():

    weth_gateway_address = "0x0fdbD7BAB654B5444c96FCc4956B8DF9CcC508bE"

    from_block = get_last_block_tracked()

    print('Last Block Number: ', from_block)
    # from_block = 940460

    tx_hash_list = []
    value_list = []
    user_address_list = []
    block_number_list = []

    i = 0
    blocks_to_cover = LATEST_BLOCK - from_block
    
    last_block_number = 0
    # adds our values to our above lists
    for block_number in range(from_block, LATEST_BLOCK + 1):
        block = web3.eth.get_block(block_number)
        tx_hashes = block.transactions

        print(i, '/', blocks_to_cover)
        i += 1

        for tx_hash in tx_hashes:
            transaction = web3.eth.get_transaction(tx_hash)
            if transaction['to'] == weth_gateway_address:
                user_address_list.append(transaction['from'])
                tx_hash_list.append(transaction['hash'].hex())
                value_list.append(transaction['value'])
                block_number_list.append(transaction['blockNumber'])
        
        last_block_number = int(block_number)
                # print('found')

    print('Last Block Number: ', last_block_number)


    # handles blank dataframes
    if len(user_address_list) < 1:
        df = pd.read_csv('all_users.csv')
        df['last_block_number'] = last_block_number

    else:
        df = pd.DataFrame()
        df['wallet_address'] = user_address_list
        df['tx_hash'] = tx_hash_list
        df['number_of_tokens'] = value_list
        df['block_number'] = block_number_list
        df['last_block_number'] = last_block_number

    make_user_data_csv(df)

get_all_gateway_transactions()

#returns our lists
def user_data(user_address, events, enum_name):
    df = pd.DataFrame()

    user_address_list = []
    tx_hash_list = []
    timestamp_list = []
    token_address_list = []
    token_volume_list = []
    token_usd_amount_list = []
    lend_borrow_type_list = []

    user = 'user'

    # start_time = time.time()
    for event in events:


        payload_address = event['args'][user].lower()
        tx_hash = event['transactionHash'].hex()
        
        if payload_address.lower() == '0x642cc899652B068D1bED786c4B060Ec1027D1563'.lower():
            if enum_name == 'LEND' or enum_name == 'BORROW':
                user = 'onBehalfOf'
                payload_address = event['args'][user].lower()


        # block = web3.eth.get_block(event['blockNumber'])
        # if block['timestamp'] >= 1701086400:
        if enum_name != 'COLLATERALISE':
            if payload_address == user_address:
                block = web3.eth.get_block(event['blockNumber'])

                user_address_list.append(payload_address)
                tx_hash_list.append(tx_hash)
                timestamp_list.append(block['timestamp'])
                token_address_list.append(event['args']['reserve'])
                token_volume_list.append(event['args']['amount'])
                # token_usd_amount_list.append(get_tx_usd_amount(event['args']['reserve'], (event['args']['amount'])))
                token_usd_amount_list.append(0)
                lend_borrow_type_list.append(enum_name)
        
        else:
            if event['args'][user].lower() == user_address:
                block = web3.eth.get_block(event['blockNumber'])

                user_address_list.append(event['args'][user].lower())
                tx_hash_list.append(event['transactionHash'].hex())
                timestamp_list.append(block['timestamp'])
                token_address_list.append(event['args']['reserve'])
                token_volume_list.append(0)
                token_usd_amount_list.append(0)
                lend_borrow_type_list.append(enum_name)
    # i = 0


    df['wallet_address'] = user_address_list
    df['txHash'] = tx_hash_list
    df['timestamp'] = timestamp_list
    df['tokenAddress'] = token_address_list
    df['tokenVolume'] = token_volume_list
    df['tokenUSDAmount'] = token_usd_amount_list
    df['lendBorrowType'] = lend_borrow_type_list

    # print('User Data Event Looping done in: ', time.time() - start_time)
    return df

#handles our weth_gateway events and returns the accurate user_address
def handle_weth_gateway(event, enum_name):

    payload_address = event['args']['user'].lower()

    if payload_address.lower() == '0x642cc899652B068D1bED786c4B060Ec1027D1563'.lower():
        if enum_name == 'LEND' or enum_name == 'BORROW':
            user = 'onBehalfOf'
            payload_address = event['args'][user].lower()
    
    return payload_address

#makes our dataframe
def user_data_2(user_address, events, enum_name):
    
    df = pd.DataFrame()

    user_address_list = []
    tx_hash_list = []
    timestamp_list = []
    token_address_list = []
    token_volume_list = []
    token_usd_amount_list = []
    lend_borrow_type_list = []

    user = ''

    start_time = time.time()
    i = 1
    print(len(events))
    for event in events:
        print(i, '/', len(events))
        i+=1
        # if enum_name == 'REPAY':
        #     user = 'user'
        # elif enum_name == 'COLLATERALISE':
        #     user = 'user'
        # else:
        #     user = 'user'

        # block = web3.eth.get_block(event['blockNumber'])
        # if block['timestamp'] >= 1701086400:
        if enum_name != 'COLLATERALISE':
            
            exists_list = already_part_of_df(event, enum_name)

            tx_hash = exists_list[0]
            wallet_address = exists_list[1]
            exists = exists_list[2]

            if exists == False and len(wallet_address) < 2:
                
                #adds wallet_address if it doesn't exist
                if len(wallet_address) < 2:
                    wallet_address = handle_weth_gateway(event, enum_name)
                

                block = web3.eth.get_block(event['blockNumber'])

                user_address_list.append(wallet_address)
                tx_hash_list.append(tx_hash)
                timestamp_list.append(block['timestamp'])
                token_address = event['args']['reserve']
                token_address_list.append(token_address)
                token_volume = event['args']['amount']
                token_volume_list.append(token_volume)
                # token_usd_amount_list.append(get_tx_usd_amount(token_address, token_volume))
                token_usd_amount_list.append(0)
                lend_borrow_type_list.append(enum_name)
            
            else:
                print('Skipped')

        else:
            exists_list = already_part_of_df(event, enum_name)

            tx_hash = exists_list[0]
            wallet_address = exists_list[1]
            exists = exists_list[2]
            
            if exists == False and len(wallet_address) < 2:
                
                wallet_address = handle_weth_gateway(event, enum_name)

                block = web3.eth.get_block(event['blockNumber'])

                user_address_list.append(wallet_address)
                tx_hash_list.append(tx_hash)
                timestamp_list.append(block['timestamp'])
                token_address_list.append(event['args']['reserve'])
                token_volume_list.append(0)
                token_usd_amount_list.append(0)
                lend_borrow_type_list.append(enum_name)
            
            else:
                print('Skipped')

    df['wallet_address'] = user_address_list
    df['txHash'] = tx_hash_list
    df['timestamp'] = timestamp_list
    df['tokenAddress'] = token_address_list
    df['tokenVolume'] = token_volume_list
    df['tokenUSDAmount'] = token_usd_amount_list
    df['lendBorrowType'] = lend_borrow_type_list

    print('User Data Event Looping done in: ', time.time() - start_time)
    return df

# will tell us whether we need to find new data
# returns a list of [tx_hash, wallet_address]
def already_part_of_df(event, enum):

    all_exist = False
    tx_hash = ''
    wallet_address = ''

    df = pd.read_csv('all_events.csv')

    tx_hash = event['transactionHash'].hex()
    tx_hash = tx_hash.lower()

    new_df = tx_hash_exists(df, tx_hash)

    if len(new_df) > 0:
        new_df = lend_borrow_type_exists(new_df, enum)

        if len(new_df) > 0:
            wallet_address = handle_weth_gateway(event, enum).lower()
            new_df = wallet_address_exists(df, wallet_address)

            if len(new_df) > 0:
                all_exist = True

    response_list = [tx_hash, wallet_address, all_exist]

    return response_list

#returns a df if a tx_hash exists
def tx_hash_exists(df, tx_hash):

    new_df = pd.DataFrame()

    if ((df['txHash'] == tx_hash)).any():
        new_df = df.loc[df['txHash'] == tx_hash]
    
    return new_df

#returns whether a enum_name exists, and returns blank df if not
def lend_borrow_type_exists(df, lend_borrow_type):

    if ((df['lendBorrowType'] == lend_borrow_type)).any():
        df = df.loc[df['lendBorrowType'] == lend_borrow_type]

    else:
        df = pd.DataFrame()

    return df

#returns df if wallet_address exists
def wallet_address_exists(df, wallet_address):

    if ((df['wallet_address'] == wallet_address)).any():
        df = df.loc[df['wallet_address'] == wallet_address]

    else:
        df = pd.DataFrame()

    return df

#gets all borrow events
# @cache
def get_borrow_events(contract):
    # latest_block = web3.eth.get_block_number()
    # from_block = latest_block - 100000
    # from_block = 1052610

    # events = contract.events.Borrow.get_logs(fromBlock=FROM_BLOCK, toBlock='latest')
    events = contract.events.borrowETH().get_logs(fromBlock=FROM_BLOCK, toBlock='latest')
    
    for event in events:
        print(event)
    return events

# get_borrow_events(get_contract())
#gets all deposit events
# @cache
def get_lend_events(contract):
    # latest_block = web3.eth.get_block_number()
    # from_block = latest_block - 100000
    # from_block = 1052610

    events = contract.events.Deposit.get_logs(fromBlock=FROM_BLOCK, toBlock='latest')
    for event in events:
        print(event)
    print('')
    return events

#gets all repay events
# @cache
def get_repay_events(contract):
    # latest_block = web3.eth.get_block_number()
    # from_block = latest_block - 100000
    # from_block = 1052610

    events = contract.events.Repay.get_logs(fromBlock=FROM_BLOCK, toBlock='latest')

    return events

#gets all collateralise events
# @cache
def get_collateralise_events(contract):
    # latest_block = web3.eth.get_block_number()
    # from_block = latest_block - 100000
    # from_block = 1052610

    events = contract.events.ReserveUsedAsCollateralEnabled.get_logs(fromBlock=FROM_BLOCK, toBlock='latest')

    return events


#gets all of our borrow transactions
# @cache
def get_borrow_transactions(user_address, contract):

    df = pd.DataFrame()

    start_time = time.time()

    events = get_borrow_events(contract)
    print('Events found in: ', time.time() - start_time)

    if len(events) > 1:
        if user_address == '0x764fdcdbca9998e5ee10b3370a74044f43ed28e2' or user_address == '0x6995fb91e61e98ae8686e299f51e0b2db7fb853b':
            try:
                # df = user_data(user_address, events, 'BORROW')
                df = user_data_2(user_address, events, 'BORROW')
            except:
                df = pd.DataFrame()
        else:
            try:
                df = user_data(user_address, events, 'BORROW')
                # df = user_data_2(user_address, events, 'BORROW')
            except:
                df = pd.DataFrame()

    return df

#gets all of our deposit transactions
# @cache
def get_lend_transactions(user_address, contract):
    
    df = pd.DataFrame()

    events = get_lend_events(contract)

    if len(events) > 1:
        if user_address == '0x764fdcdbca9998e5ee10b3370a74044f43ed28e2' or user_address == '0x6995fb91e61e98ae8686e299f51e0b2db7fb853b':
            try:
                # df = user_data(user_address, events, 'LEND')
                df = user_data_2(user_address, events, 'LEND')
            except:
                df = pd.DataFrame()
        else:
            try:
                df = user_data(user_address, events, 'LEND')
                # df = user_data_2(user_address, events, 'LEND')
            except:
                df = pd.DataFrame()

    return df

#gets all of our repayment transactions
# @cache
def get_repay_transactions(user_address, contract):

    df = pd.DataFrame()


    events = get_repay_events(contract)

    if len(events) > 1:
        if user_address == '0x764fdcdbca9998e5ee10b3370a74044f43ed28e2' or user_address == '0x6995fb91e61e98ae8686e299f51e0b2db7fb853b':
            try:
                # df = user_data(user_address, events, 'REPAY')
                df = user_data_2(user_address, events, 'REPAY')
            except:
                df = pd.DataFrame()
        else:
            try:
                df = user_data(user_address, events, 'REPAY')
                # df = user_data_2(user_address, events, 'REPAY')
            except:
                df = pd.DataFrame()
    
    return df

# @cache
def get_collateralalise_transactions(user_address, contract):
    
    df = pd.DataFrame()
    
    events = get_collateralise_events(contract)
    if len(events) > 1:
        if user_address == '0x764fdcdbca9998e5ee10b3370a74044f43ed28e2' or user_address == '0x6995fb91e61e98ae8686e299f51e0b2db7fb853b':
            try:
                # df = user_data(user_address, events, 'COLLATERALISE')
                df = user_data_2(user_address, events, 'COLLATERALISE')
            except:
                df = pd.DataFrame()
        else:
            try:
                df = user_data(user_address, events, 'COLLATERALISE')
                # df = user_data_2(user_address, events, 'COLLATERALISE')
            except:
                df = pd.DataFrame()

    return df

#takes in our user address and will populate all the needed fields for our api_response
# @cache
def get_all_user_transactions(user_address):

    df = pd.DataFrame()

    df_list = []

    if len(user_address) == 42:
        contract = get_contract()

        start_time = time.time()
        borrow_df = get_borrow_transactions(user_address, contract)
        # print(borrow_df)
        make_user_data_csv(borrow_df)
        print('Borrower Transactions found in: ', time.time() - start_time)
        start_time = time.time()
        lend_df = get_lend_transactions(user_address, contract)
        make_user_data_csv(lend_df)
        print(lend_df)
        print('Lend Transactions found in: ', time.time() - start_time)
        start_time = time.time()
        repay_df = get_repay_transactions(user_address, contract)
        make_user_data_csv(repay_df)
        # print(repay_df)
        print('Repay Transactions found in: ', time.time() - start_time)
        start_time = time.time()
        collateralize_df = get_collateralalise_transactions(user_address, contract)
        make_user_data_csv(collateralize_df)
        # print(collateralize_df)
        print('Collaterise Transactions found in: ', time.time() - start_time)

        # properly redoes our collateralizes
        handle_gateway_collateralise()

        # df_list = [borrow_df, lend_df, repay_df, collateralize_df]

        df_list = [lend_df]

        df = pd.concat(df_list)
    
    # print(df)

    return df

# formats our dataframe response
def make_api_response_string(df):
    
    data = []

    #if we have an address with no transactions
    if len(df) < 1:
        temp_df = pd.DataFrame()
        data.append({
           "txHash": 'N/A',
            "timestamp": -1,
            "tokenAddress": 'N/A',
            "tokenVolume": '-1',
            "tokenUSDAmount": -1,
            "lendBorrowType": 'N/A'
        })

    else:
        temp_df = df[['txHash', 'timestamp', 'tokenAddress', 'tokenVolume', 'tokenUSDAmount', 'lendBorrowType']]
        # Process data
        for i in range(temp_df.shape[0]):
            row = temp_df.iloc[i]
            data.append({
                "txHash": str(row['txHash']),
                "timestamp": int(row['timestamp']),
                "tokenAddress": str(row['tokenAddress']),
                "tokenVolume": str(row['tokenVolume']),
                "tokenUSDAmount": float(row['tokenUSDAmount']),
                "lendBorrowType": str(row['lendBorrowType'])
            })

    # Create JSON response
    response = {
        "error": {
            "code": 0,
            "message": "success"
        },
        "data": {
            "result": data
        }
    }
    
    return response

# executes all of functions
def search_and_respond(address, queue):

    df = get_all_user_transactions(address)
    
    response = make_api_response_string(df)

    queue.put(response)

    queue.join()

    make_user_data_csv(df)
    # return response

#just reads from csv file
def search_and_respond_2(address, queue):
    
    df = pd.read_csv('all_events.csv')

    df = df.loc[df['wallet_address'] == address]

    response = make_api_response_string(df)

    queue.put(response)

    #new_df = get_all_user_transactions(address)

    #make_user_data_csv(new_df)

#gets rid of weth_gateway_collateralizes
# adds a collateral row for each lend row for users who have borrowed something
# removes duplicates
def handle_gateway_collateralise():
    df = pd.read_csv('all_events.csv')
    df['wallet_address'] = df['wallet_address'].str.lower()
    df['txHash'] = df['txHash'].str.lower()

    df = df[df.wallet_address != '0x642cc899652B068D1bED786c4B060Ec1027D1563']

    lend_df = df.loc[df['lendBorrowType'] == 'LEND']

    borrow_df = df.loc[df['lendBorrowType'] == 'BORROW']

    borrower_wallet_list = borrow_df['wallet_address'].tolist()

    #gives us only wallet addresses that have borrowed something
    #this means that the user should have 'collateralized' some of their assets to begin with
    lend_df = lend_df[lend_df['wallet_address'].isin(borrower_wallet_list)]

    collateralize_df = lend_df

    collateralize_df['tokenVolume'] = '0'
    collateralize_df['tokenUSDAmount'] = 0
    collateralize_df['lendBorrowType'] = 'COLLATERALISE'

    make_user_data_csv(collateralize_df)

    return

#reads from csv
@app.route("/transactions/", methods=["POST"])
def get_transactions():

    data = json.loads(request.data)  # Parse JSON string into JSON object

    print(data)
    address = data['address']
    address = address.lower()
    print(address)

    # Create a queue to store the search result
    result_queue = queue.Queue()

    thread = threading.Thread(target=search_and_respond_2, args=(address, result_queue))
    thread.start()
    
    response = result_queue.get()

    return jsonify(response), 200

#get v3
#makes our csv
@app.route("/test/<address>", methods=["GET"])
def balance_of(address):
    
    address = address.lower()

    df = get_all_user_transactions(address)

    response = make_api_response_string(df)

    # Create a queue to store the search result
    result_queue = queue.Queue()

    thread = threading.Thread(target=search_and_respond, args=(address, result_queue))
    thread.start()
    
    response = result_queue.get()

    return jsonify(response), 200

# print(get_all_user_transactions('0xdd66f8ee84c30aefec2137e2c1133503d5721bb2'))
# print(get_all_user_transactions('0x764fdcdbca9998e5ee10b3370a74044f43ed28e2'))
# print('2')

# 0x764fdcdbca9998e5ee10b3370a74044f43ed28e2
# if __name__ == "__main__":
#     app.run()
