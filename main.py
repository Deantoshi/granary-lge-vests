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

# # Borrow USDC tx: https://eon-explorer.horizenlabs.io/tx/0xa053e235cec7c46b7cc90c92d17abdaec1786b17230ed64835c2a76f2cf95acd
# # Deposit USDC tx: https://eon-explorer.horizenlabs.io/tx/0xddcd860b32605a558e1e244ace4b970aab5b88c74449eb10e720b0d78af8253b
# # Borrow BTC tx: https://eon-explorer.horizenlabs.io/tx/0xf6c930a259680c81b35738d9e1982cd9a0b2f5767920d6d0a5a526e912841fec
# # Deposit BTC tx: https://eon-explorer.horizenlabs.io/tx/0x9be4cac88854d04f6ea10389bf9fcecad8aae7155905a501c13e037228377e19
# # Borrow ETH tx: https://eon-explorer.horizenlabs.io/tx/0x28fd834d498c5ee3f5f4f8b00be6dcec876906e16e3870a5d51d693c2952dea9
# # Deposit ETH tx: https://eon-explorer.horizenlabs.io/tx/0x164213e475b2a4c70325c3d75426c4aa0a9e0fe1b1eeb2b9a46c6c83e93a8796
# # Deposit ZEN tx: https://eon-explorer.horizenlabs.io/tx/0x6cd3d731c1a46f238288abb9c5769b06336281225114e5d2c1a9a234781fa1e4
# # Borrow ZEN tx: https://eon-explorer.horizenlabs.io/tx/0xb6acca9fabb43ee466a822aa6cb68dd89b52c6cb876ccd7bf554f5da7e049308

app = Flask(__name__)

# Replace with the actual Optimism RPC URL
optimism_rpc_url = 'https://eon-rpc.horizenlabs.io/ethv1'

# Create a Web3 instance to connect to the Optimism blockchain
web3 = Web3(Web3.HTTPProvider(optimism_rpc_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

# LATEST_BLOCK = web3.eth.get_block_number()
LATEST_BLOCK = 951714 + 1
FROM_BLOCK = 951714
# FROM_BLOCK = 0

# Replace with the actual Aave V2 contract address
# contract_address = "0x871AfF0013bE6218B61b28b274a6F53DB131795F"


# returns basic data about our reserves in a dataframe
def get_reserve_data():
    
    reserve_address_list = ['0xeb329420fae03176ec5877c34e2c38580d85e069', '0xbe8afe7e442ffffe576b979d490c5adb7823c3c6', '0x1d6492faacb1ea15641dd94fb9ab020056abbc94', '0xa0cd598ef64856502ae294aa58bfed90922fb3c7', 
                    '0x6c29836be0dcd891c1c4ca77ff8f3a29e4a3fa5e', '0x770d3ed41f9f57ebb0463bd435df7fcc6f1e40ce', '0x3f8f2929a2a461d4b59575f132016348cf526f25', '0xbc25f58ba700452d66d1e025de6abfd23a659265']

    reserve_decimal_list = [1e18, 1e18, 1e6, 1e6, 1e8, 1e8, 1e18, 1e18]

    reserve_name_list = ['a_zen', 'v_zen', 'v_usdc', 'a_usdc', 'v_wbtc', 'a_wbtc', 'v_weth', 'a_weth']

    df = pd.DataFrame()

    df['reserve_name'] = reserve_name_list
    df['reserve_address'] = reserve_address_list
    df['reserve_decimal'] = reserve_decimal_list

    return df
    # reserve_list = [x.lower() for x in reserve_list]

    decimals = 0

    # if reserve_address == '0xEB329420Fae03176EC5877c34E2c38580D85E069'.lower(): # yuzuZen
    #     decimals = 1e18
    
    # if reserve_address == '0xBE8afE7E442fFfFE576B979D490c5ADb7823C3c6'.lower(): # v_debt_yuzu
    #     decimals = 1e18

    # elif reserve_address == '0x1d6492FaAcB1ea15641dD94FB9AB020056aBBC94'.lower(): # v_debt_usdc
    #     decimals = 1e6
    
    # elif reserve_address == '0xA0cD598EF64856502aE294aa58bFEd90922Fb3c7'.lower(): # yuzu_usdc
    #     decimals = 1e6
    
    # elif reserve_address == '0x6c29836bE0DCD891C1c4CA77ff8F3A29e4A3Fa5E'.lower(): # v_debt_wbtc
    #     decimals = 1e8
    
    # elif reserve_address == '0x770D3eD41f9F57eBB0463Bd435DF7FCc6f1e40Ce'.lower(): # yuzu_wbtc
    #     decimals = 1e8
    
    # elif reserve_address == '0x3f8F2929a2A461d4B59575F132016348CF526F25'.lower(): # v_debt_weth
    #     decimals = 1e18
    
    # elif reserve_address == '0xbc25f58bA700452D66d1E025De6aBFd23a659265'.lower(): # yuzu_weth
    #     decimals = 1e18
    


    

    
    # return decimals

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

# print(get_last_block_tracked())

#makes a dataframe and stores it in a csv file
def make_user_data_csv(df):
    old_df = pd.read_csv('all_users.csv')
    old_df = old_df.drop_duplicates(subset=['wallet_address','tx_hash','number_of_tokens','block_number'], keep='last')

    combined_df_list = [df, old_df]

    combined_df = pd.concat(combined_df_list)
    combined_df = combined_df.drop_duplicates(subset=['wallet_address','tx_hash','number_of_tokens','block_number'], keep='last')

    combined_df['tx_hash'] = combined_df['tx_hash'].str.lower()
    combined_df['wallet_address'] = combined_df['wallet_address'].str.lower()

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

# handles our csv writing
def make_transactions_csv(df):
    old_df = pd.read_csv('user_transactions.csv')
    old_df = old_df.drop_duplicates(subset=['wallet_address','token_name','number_of_tokens','reserve_address','tx_hash','block_number'], keep='last')

    combined_df_list = [df, old_df]

    combined_df = pd.concat(combined_df_list)
    combined_df = combined_df.drop_duplicates(subset=['wallet_address','token_name','number_of_tokens','reserve_address','tx_hash','block_number'], keep='last')

    print(combined_df.dtypes)
    combined_df['tx_hash'] = combined_df['tx_hash'].str.lower()
    combined_df['wallet_address'] = combined_df['wallet_address'].str.lower()

    if len(combined_df) >= len(old_df):
        combined_df['last_block_number'] = int(df['last_block_number'].max())
        combined_df.to_csv('user_transactions.csv', index=False)
        print('CSV Made')

    elif len(combined_df) > 0:
        combined_df['last_block_number'] = int(df['last_block_number'].max())
        combined_df.to_csv('user_transactions.csv', index=False)
        print('CSV Made')
    
    return

# # takes in an a_token address and returns it's contract object
def get_a_token_contract(contract_address):
    # contract_address = "0xEB329420Fae03176EC5877c34E2c38580D85E069"
    contract_abi = [{"type":"event","name":"Approval","inputs":[{"type":"address","name":"owner","internalType":"address","indexed":True},{"type":"address","name":"spender","internalType":"address","indexed":True},{"type":"uint256","name":"value","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"BalanceTransfer","inputs":[{"type":"address","name":"from","internalType":"address","indexed":True},{"type":"address","name":"to","internalType":"address","indexed":True},{"type":"uint256","name":"value","internalType":"uint256","indexed":False},{"type":"uint256","name":"index","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"Burn","inputs":[{"type":"address","name":"from","internalType":"address","indexed":True},{"type":"address","name":"target","internalType":"address","indexed":True},{"type":"uint256","name":"value","internalType":"uint256","indexed":False},{"type":"uint256","name":"index","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"Initialized","inputs":[{"type":"address","name":"underlyingAsset","internalType":"address","indexed":True},{"type":"address","name":"pool","internalType":"address","indexed":True},{"type":"address","name":"treasury","internalType":"address","indexed":False},{"type":"address","name":"incentivesController","internalType":"address","indexed":False},{"type":"uint8","name":"aTokenDecimals","internalType":"uint8","indexed":False},{"type":"string","name":"aTokenName","internalType":"string","indexed":False},{"type":"string","name":"aTokenSymbol","internalType":"string","indexed":False},{"type":"bytes","name":"params","internalType":"bytes","indexed":False}],"anonymous":False},{"type":"event","name":"Mint","inputs":[{"type":"address","name":"from","internalType":"address","indexed":True},{"type":"uint256","name":"value","internalType":"uint256","indexed":False},{"type":"uint256","name":"index","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"Transfer","inputs":[{"type":"address","name":"from","internalType":"address","indexed":True},{"type":"address","name":"to","internalType":"address","indexed":True},{"type":"uint256","name":"value","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"ATOKEN_REVISION","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"bytes32","name":"","internalType":"bytes32"}],"name":"DOMAIN_SEPARATOR","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"bytes","name":"","internalType":"bytes"}],"name":"EIP712_REVISION","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"bytes32","name":"","internalType":"bytes32"}],"name":"PERMIT_TYPEHASH","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"contract ILendingPool"}],"name":"POOL","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"RESERVE_TREASURY_ADDRESS","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"UNDERLYING_ASSET_ADDRESS","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"_nonces","inputs":[{"type":"address","name":"","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"allowance","inputs":[{"type":"address","name":"owner","internalType":"address"},{"type":"address","name":"spender","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"approve","inputs":[{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"balanceOf","inputs":[{"type":"address","name":"user","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"burn","inputs":[{"type":"address","name":"user","internalType":"address"},{"type":"address","name":"receiverOfUnderlying","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"},{"type":"uint256","name":"index","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint8","name":"","internalType":"uint8"}],"name":"decimals","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"decreaseAllowance","inputs":[{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"subtractedValue","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"contract IRewarder"}],"name":"getIncentivesController","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"},{"type":"uint256","name":"","internalType":"uint256"}],"name":"getScaledUserBalanceAndSupply","inputs":[{"type":"address","name":"user","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"handleRepayment","inputs":[{"type":"address","name":"user","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"increaseAllowance","inputs":[{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"addedValue","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"initialize","inputs":[{"type":"address","name":"pool","internalType":"contract ILendingPool"},{"type":"address","name":"treasury","internalType":"address"},{"type":"address","name":"underlyingAsset","internalType":"address"},{"type":"address","name":"incentivesController","internalType":"contract IRewarder"},{"type":"uint8","name":"aTokenDecimals","internalType":"uint8"},{"type":"string","name":"aTokenName","internalType":"string"},{"type":"string","name":"aTokenSymbol","internalType":"string"},{"type":"bytes","name":"params","internalType":"bytes"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"mint","inputs":[{"type":"address","name":"user","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"},{"type":"uint256","name":"index","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"mintToTreasury","inputs":[{"type":"uint256","name":"amount","internalType":"uint256"},{"type":"uint256","name":"index","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"name","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"permit","inputs":[{"type":"address","name":"owner","internalType":"address"},{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"value","internalType":"uint256"},{"type":"uint256","name":"deadline","internalType":"uint256"},{"type":"uint8","name":"v","internalType":"uint8"},{"type":"bytes32","name":"r","internalType":"bytes32"},{"type":"bytes32","name":"s","internalType":"bytes32"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"scaledBalanceOf","inputs":[{"type":"address","name":"user","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"scaledTotalSupply","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"symbol","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalSupply","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"transfer","inputs":[{"type":"address","name":"recipient","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"transferFrom","inputs":[{"type":"address","name":"sender","internalType":"address"},{"type":"address","name":"recipient","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"transferOnLiquidation","inputs":[{"type":"address","name":"from","internalType":"address"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"value","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"transferUnderlyingTo","inputs":[{"type":"address","name":"target","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"}]}]
    
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    return contract

# # takes in an v_token address and returns it's contract object
def get_v_token_contract(contract_address):
    # contract_address = "0xBE8afE7E442fFfFE576B979D490c5ADb7823C3c6"
    contract_abi = [{"type":"event","name":"Approval","inputs":[{"type":"address","name":"owner","internalType":"address","indexed":True},{"type":"address","name":"spender","internalType":"address","indexed":True},{"type":"uint256","name":"value","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"BorrowAllowanceDelegated","inputs":[{"type":"address","name":"fromUser","internalType":"address","indexed":True},{"type":"address","name":"toUser","internalType":"address","indexed":True},{"type":"address","name":"asset","internalType":"address","indexed":False},{"type":"uint256","name":"amount","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"Burn","inputs":[{"type":"address","name":"user","internalType":"address","indexed":True},{"type":"uint256","name":"amount","internalType":"uint256","indexed":False},{"type":"uint256","name":"currentBalance","internalType":"uint256","indexed":False},{"type":"uint256","name":"balanceIncrease","internalType":"uint256","indexed":False},{"type":"uint256","name":"avgStableRate","internalType":"uint256","indexed":False},{"type":"uint256","name":"newTotalSupply","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"Initialized","inputs":[{"type":"address","name":"underlyingAsset","internalType":"address","indexed":True},{"type":"address","name":"pool","internalType":"address","indexed":True},{"type":"address","name":"incentivesController","internalType":"address","indexed":False},{"type":"uint8","name":"debtTokenDecimals","internalType":"uint8","indexed":False},{"type":"string","name":"debtTokenName","internalType":"string","indexed":False},{"type":"string","name":"debtTokenSymbol","internalType":"string","indexed":False},{"type":"bytes","name":"params","internalType":"bytes","indexed":False}],"anonymous":False},{"type":"event","name":"Mint","inputs":[{"type":"address","name":"user","internalType":"address","indexed":True},{"type":"address","name":"onBehalfOf","internalType":"address","indexed":True},{"type":"uint256","name":"amount","internalType":"uint256","indexed":False},{"type":"uint256","name":"currentBalance","internalType":"uint256","indexed":False},{"type":"uint256","name":"balanceIncrease","internalType":"uint256","indexed":False},{"type":"uint256","name":"newRate","internalType":"uint256","indexed":False},{"type":"uint256","name":"avgStableRate","internalType":"uint256","indexed":False},{"type":"uint256","name":"newTotalSupply","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"Transfer","inputs":[{"type":"address","name":"from","internalType":"address","indexed":True},{"type":"address","name":"to","internalType":"address","indexed":True},{"type":"uint256","name":"value","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"DEBT_TOKEN_REVISION","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"contract ILendingPool"}],"name":"POOL","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"UNDERLYING_ASSET_ADDRESS","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"allowance","inputs":[{"type":"address","name":"owner","internalType":"address"},{"type":"address","name":"spender","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"approve","inputs":[{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"approveDelegation","inputs":[{"type":"address","name":"delegatee","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"balanceOf","inputs":[{"type":"address","name":"account","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"borrowAllowance","inputs":[{"type":"address","name":"fromUser","internalType":"address"},{"type":"address","name":"toUser","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"burn","inputs":[{"type":"address","name":"user","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint8","name":"","internalType":"uint8"}],"name":"decimals","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"decreaseAllowance","inputs":[{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"subtractedValue","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"getAverageStableRate","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"contract IRewarder"}],"name":"getIncentivesController","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"},{"type":"uint256","name":"","internalType":"uint256"},{"type":"uint256","name":"","internalType":"uint256"},{"type":"uint40","name":"","internalType":"uint40"}],"name":"getSupplyData","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"},{"type":"uint256","name":"","internalType":"uint256"}],"name":"getTotalSupplyAndAvgRate","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint40","name":"","internalType":"uint40"}],"name":"getTotalSupplyLastUpdated","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint40","name":"","internalType":"uint40"}],"name":"getUserLastUpdated","inputs":[{"type":"address","name":"user","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"getUserStableRate","inputs":[{"type":"address","name":"user","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"increaseAllowance","inputs":[{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"addedValue","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"initialize","inputs":[{"type":"address","name":"pool","internalType":"contract ILendingPool"},{"type":"address","name":"underlyingAsset","internalType":"address"},{"type":"address","name":"incentivesController","internalType":"contract IRewarder"},{"type":"uint8","name":"debtTokenDecimals","internalType":"uint8"},{"type":"string","name":"debtTokenName","internalType":"string"},{"type":"string","name":"debtTokenSymbol","internalType":"string"},{"type":"bytes","name":"params","internalType":"bytes"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"mint","inputs":[{"type":"address","name":"user","internalType":"address"},{"type":"address","name":"onBehalfOf","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"},{"type":"uint256","name":"rate","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"name","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"principalBalanceOf","inputs":[{"type":"address","name":"user","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"symbol","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalSupply","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"transfer","inputs":[{"type":"address","name":"recipient","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"transferFrom","inputs":[{"type":"address","name":"sender","internalType":"address"},{"type":"address","name":"recipient","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"}]}]    
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    return contract

# # takes in a contract object and returns all associated events
def get_yuzu_events(contract):
    
    events = contract.events.Transfer.get_logs(fromBlock=FROM_BLOCK, toBlock=LATEST_BLOCK)
    
    return events

# # first quest that will add column to df and specify 0 as False and 1 as true
def user_made_transaction(df):
    df['user_made_transaction'] = 1
    return df

# # takes in our whole dataframe, wallet_address, reserve_address, minimum_tokens
# # will return whether the user has a transaction for a certain token that passes that token's minimum transfer
# # example: Can check whether a user has deposited 10 zen in one transaction
def is_quest_completed(df, wallet_address, reserve_address, minimum_tokens):

    df = df.loc[df['wallet_address'] == wallet_address]
    df = df.loc[df['reserve_address'] == reserve_address]

    is_completed = -1

    if len(df) > 0:
        tokens_transacted = df['number_of_tokens'].max()

        if tokens_transacted >= minimum_tokens:
            is_completed = 1
    
    else:
        is_completed = 0

    return is_completed

# # Second quest that will add column to df and specify 0 as False and 1 as true
# # User deposited 10 Zen in one transaction
def user_deposited_10_zen(df, wallet_address):

    reserve_address = '0xeb329420fae03176ec5877c34e2c38580d85e069'
    minimum_tokens = 10
    quest_name = '10_zen_deposited'

    is_completed = is_quest_completed(wallet_address, reserve_address, minimum_tokens, quest_name)


    return df

df = pd.read_csv('user_transactions.csv')

completed = is_quest_completed(df, '0x54f7d603881d850a83ec29e2a1dd61e4d0b8d58a', '0xeb329420fae03176ec5877c34e2c38580d85e069', 0.00001)

# # takes in an events object and returns a dataframe with relevent transaction output
def get_transaction_data(events, reserve_df):

    user_address_list = []
    token_name_list = []
    token_address_list = []
    token_amount_list = []
    block_number_list = []
    tx_hash_list = []

    all_block_list = []

    for event in events:
        tx_from = event['args']['from'].lower()
        tx_to = event['args']['to'].lower()

        if tx_from == "0x0000000000000000000000000000000000000000" and tx_to != "0x0fdbD7BAB654B5444c96FCc4956B8DF9CcC508bE".lower():
            token_address = event['address'].lower()
            token_amount = event['args']['value']
            temp_df = reserve_df.loc[reserve_df['reserve_address'] == token_address]

            # get whole numbers of our token amount
            token_amount = round(token_amount / temp_df['reserve_decimal'].iloc[0], 5)
            token_name = temp_df['reserve_name'].iloc[0]
            block_number = int(event['blockNumber'])

            print(event)
            user_address_list.append(tx_to)
            token_name_list.append(token_name)
            token_address_list.append(token_address)
            token_amount_list.append(token_amount)
            block_number_list.append(block_number)

            all_block_list.append(block_number)

            tx_hash_list.append(event['transactionHash'].hex().lower())
        
        elif tx_from == "0x0000000000000000000000000000000000000000" and tx_to == "0x0fdbD7BAB654B5444c96FCc4956B8DF9CcC508bE".lower():
            print('WETH Gateway Transaction Found!')
            print(event)

    df = pd.DataFrame()

    df['wallet_address'] = user_address_list
    df['token_name'] = token_name_list
    df['number_of_tokens'] = token_amount_list
    df['reserve_address'] = token_address_list
    df['tx_hash'] = tx_hash_list
    df['block_number'] = block_number_list

    df['last_block_number'] = max(block_number_list)

    df[['wallet_address', 'token_name', 'reserve_address', 'tx_hash']] = df[['wallet_address', 'token_name', 'reserve_address', 'tx_hash']].astype(str)

    #handles our transactions
    make_transactions_csv(df)
    # df.to_csv('user_transactions.csv', index=False)
    return


contract_address = '0xEB329420Fae03176EC5877c34E2c38580D85E069'
reserve_df = get_reserve_data()
contract = get_a_token_contract(contract_address)
events = get_yuzu_events(contract)
get_transaction_data(events, reserve_df)



# Gets transactions of all blocks within a specified range and returns a df with info from blocks that include our contract
def get_all_gateway_transactions():

    weth_gateway_address = "0x0fdbD7BAB654B5444c96FCc4956B8DF9CcC508bE"

    # from_block = get_last_block_tracked()

    from_block = 946990

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
            print(transaction)
            print('')
            if transaction['to'] == weth_gateway_address:
               # print(transaction)
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

# get_all_gateway_transactions()

#gets the ids of all twitter followers of yuzu
# twitter api yahooooooo
def get_all_twitter_follows():
    return


# formats our dataframe response
def make_api_response_string(df):
    
    data = []

    quest_complete = 'False'

    #if we have an address with no transactions
    if len(df) < 1:
        quest_complete = 'False'

    else:
        quest_complete = 'True'

    # Create JSON response
    response = {
        "error": {
            "code": 0,
            "message": "success"
        },
        "data": {
            "result": quest_complete
        }
    }
    
    return response

# reads csv for twitter kids
def search_and_respond(twitter_id, queue):

    df = pd.read_csv('twitter_users.csv')

    df = df.loc[df['follower_id'] == twitter_id]

    response = make_api_response_string(df)

    queue.put(response)

# just reads from csv file
def search_and_respond_2(address, queue):
    
    df = pd.read_csv('all_users.csv')

    df = df.loc[df['wallet_address'] == address]

    response = make_api_response_string(df)

    queue.put(response)

#reads from csv
@app.route("/transactions/", methods=["POST"])
def get_transactions():

    data = json.loads(request.data)  # Parse JSON string into JSON object

    #used to help determine if we received an address or a twitter profile
    is_address = True

    if "address" in data:
        address = data["address"].lower()
        response = "Address Sent"
        print("Address Sent")
        is_address = True

    elif "twitter" in data:
        twitter = data["twitter"].lower()
        response = "Twitter Sent"
        print("Twitter Sent")
        is_address = False

    # Create a queue to store the search result
    result_queue = queue.Queue()

    # search_and_respond_2(address, result_queue)
    if is_address == True:
        thread = threading.Thread(target=search_and_respond_2, args=(address, result_queue))
        thread.start()
    
    else:
        thread = threading.Thread(target=search_and_respond, args=(twitter, result_queue))
        thread.start()
    response = result_queue.get()

    return jsonify(response), 200

# if __name__ == "__main__":
#     app.run()

# get_all_gateway_transactions()
