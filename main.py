from web3 import Web3
from web3.middleware import geth_poa_middleware 
import pandas as pd
import time

# Replace with the actual Optimism RPC URL
# rpc_url = 'https://andromeda.metis.io'
rpc_url = 'https://gateway.tenderly.co/public/optimism'

# Create a Web3 instance to connect to the Optimism blockchain
# web3 = Web3(Web3.HTTPProvider(rpc_url))
# web3.middleware_onion.inject(geth_poa_middleware, layer=0)

# LATEST_BLOCK = web3.eth.get_block_number()
LATEST_BLOCK = 951714 + 1
#Lending pool founding block
# FROM_BLOCK = 758632
FROM_BLOCK = 778064
# FROM_BLOCK = 0

#gets our web3 contract object
# @cache
def get_contract():
    contract_address = "0x871AfF0013bE6218B61b28b274a6F53DB131795F"
    contract_abi = [{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"reserve","type":"address"},{"indexed":False,"internalType":"address","name":"user","type":"address"},{"indexed":True,"internalType":"address","name":"onBehalfOf","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"borrowRateMode","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"borrowRate","type":"uint256"},{"indexed":True,"internalType":"uint16","name":"referral","type":"uint16"}],"name":"Borrow","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"reserve","type":"address"},{"indexed":False,"internalType":"address","name":"user","type":"address"},{"indexed":True,"internalType":"address","name":"onBehalfOf","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":True,"internalType":"uint16","name":"referral","type":"uint16"}],"name":"Deposit","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"target","type":"address"},{"indexed":True,"internalType":"address","name":"initiator","type":"address"},{"indexed":True,"internalType":"address","name":"asset","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"premium","type":"uint256"},{"indexed":False,"internalType":"uint16","name":"referralCode","type":"uint16"}],"name":"FlashLoan","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"collateralAsset","type":"address"},{"indexed":True,"internalType":"address","name":"debtAsset","type":"address"},{"indexed":True,"internalType":"address","name":"user","type":"address"},{"indexed":False,"internalType":"uint256","name":"debtToCover","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"liquidatedCollateralAmount","type":"uint256"},{"indexed":False,"internalType":"address","name":"liquidator","type":"address"},{"indexed":False,"internalType":"bool","name":"receiveAToken","type":"bool"}],"name":"LiquidationCall","type":"event"},{"anonymous":False,"inputs":[],"name":"Paused","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"reserve","type":"address"},{"indexed":True,"internalType":"address","name":"user","type":"address"}],"name":"RebalanceStableBorrowRate","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"reserve","type":"address"},{"indexed":True,"internalType":"address","name":"user","type":"address"},{"indexed":True,"internalType":"address","name":"repayer","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Repay","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"reserve","type":"address"},{"indexed":False,"internalType":"uint256","name":"liquidityRate","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"stableBorrowRate","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"variableBorrowRate","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"liquidityIndex","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"variableBorrowIndex","type":"uint256"}],"name":"ReserveDataUpdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"reserve","type":"address"},{"indexed":True,"internalType":"address","name":"user","type":"address"}],"name":"ReserveUsedAsCollateralDisabled","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"reserve","type":"address"},{"indexed":True,"internalType":"address","name":"user","type":"address"}],"name":"ReserveUsedAsCollateralEnabled","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"reserve","type":"address"},{"indexed":True,"internalType":"address","name":"user","type":"address"},{"indexed":False,"internalType":"uint256","name":"rateMode","type":"uint256"}],"name":"Swap","type":"event"},{"anonymous":False,"inputs":[],"name":"Unpaused","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"reserve","type":"address"},{"indexed":True,"internalType":"address","name":"user","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"FLASHLOAN_PREMIUM_TOTAL","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"LENDINGPOOL_REVISION","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MAX_NUMBER_RESERVES","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MAX_STABLE_RATE_BORROW_SIZE_PERCENT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"interestRateMode","type":"uint256"},{"internalType":"uint16","name":"referralCode","type":"uint16"},{"internalType":"address","name":"onBehalfOf","type":"address"}],"name":"borrow","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"onBehalfOf","type":"address"},{"internalType":"uint16","name":"referralCode","type":"uint16"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"balanceFromBefore","type":"uint256"},{"internalType":"uint256","name":"balanceToBefore","type":"uint256"}],"name":"finalizeTransfer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"receiverAddress","type":"address"},{"internalType":"address[]","name":"assets","type":"address[]"},{"internalType":"uint256[]","name":"amounts","type":"uint256[]"},{"internalType":"uint256[]","name":"modes","type":"uint256[]"},{"internalType":"address","name":"onBehalfOf","type":"address"},{"internalType":"bytes","name":"params","type":"bytes"},{"internalType":"uint16","name":"referralCode","type":"uint16"}],"name":"flashLoan","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getAddressesProvider","outputs":[{"internalType":"contract ILendingPoolAddressesProvider","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"}],"name":"getConfiguration","outputs":[{"components":[{"internalType":"uint256","name":"data","type":"uint256"}],"internalType":"struct DataTypes.ReserveConfigurationMap","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"}],"name":"getReserveData","outputs":[{"components":[{"components":[{"internalType":"uint256","name":"data","type":"uint256"}],"internalType":"struct DataTypes.ReserveConfigurationMap","name":"configuration","type":"tuple"},{"internalType":"uint128","name":"liquidityIndex","type":"uint128"},{"internalType":"uint128","name":"variableBorrowIndex","type":"uint128"},{"internalType":"uint128","name":"currentLiquidityRate","type":"uint128"},{"internalType":"uint128","name":"currentVariableBorrowRate","type":"uint128"},{"internalType":"uint128","name":"currentStableBorrowRate","type":"uint128"},{"internalType":"uint40","name":"lastUpdateTimestamp","type":"uint40"},{"internalType":"address","name":"aTokenAddress","type":"address"},{"internalType":"address","name":"stableDebtTokenAddress","type":"address"},{"internalType":"address","name":"variableDebtTokenAddress","type":"address"},{"internalType":"address","name":"interestRateStrategyAddress","type":"address"},{"internalType":"uint8","name":"id","type":"uint8"}],"internalType":"struct DataTypes.ReserveData","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"}],"name":"getReserveNormalizedIncome","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"}],"name":"getReserveNormalizedVariableDebt","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getReservesList","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getUserAccountData","outputs":[{"internalType":"uint256","name":"totalCollateralETH","type":"uint256"},{"internalType":"uint256","name":"totalDebtETH","type":"uint256"},{"internalType":"uint256","name":"availableBorrowsETH","type":"uint256"},{"internalType":"uint256","name":"currentLiquidationThreshold","type":"uint256"},{"internalType":"uint256","name":"ltv","type":"uint256"},{"internalType":"uint256","name":"healthFactor","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getUserConfiguration","outputs":[{"components":[{"internalType":"uint256","name":"data","type":"uint256"}],"internalType":"struct DataTypes.UserConfigurationMap","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"address","name":"aTokenAddress","type":"address"},{"internalType":"address","name":"stableDebtAddress","type":"address"},{"internalType":"address","name":"variableDebtAddress","type":"address"},{"internalType":"address","name":"interestRateStrategyAddress","type":"address"}],"name":"initReserve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract ILendingPoolAddressesProvider","name":"provider","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"collateralAsset","type":"address"},{"internalType":"address","name":"debtAsset","type":"address"},{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"debtToCover","type":"uint256"},{"internalType":"bool","name":"receiveAToken","type":"bool"}],"name":"liquidationCall","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"address","name":"user","type":"address"}],"name":"rebalanceStableBorrowRate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"rateMode","type":"uint256"},{"internalType":"address","name":"onBehalfOf","type":"address"}],"name":"repay","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"uint256","name":"configuration","type":"uint256"}],"name":"setConfiguration","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"val","type":"bool"}],"name":"setPause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"address","name":"rateStrategyAddress","type":"address"}],"name":"setReserveInterestRateStrategyAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"bool","name":"useAsCollateral","type":"bool"}],"name":"setUserUseReserveAsCollateral","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"uint256","name":"rateMode","type":"uint256"}],"name":"swapBorrowRateMode","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"to","type":"address"}],"name":"withdraw","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"}]
    
    # Create contract instance
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    return contract

# gets the last block number we have gotten data from and returns this block number
def get_last_block_tracked():
    df = pd.read_csv('all_users.csv')
    
    last_block_monitored = df['last_block_number'].max()

    last_block_monitored = int(last_block_monitored)

    return last_block_monitored

# print(get_last_block_tracked())

# # gets our token_id that will be used in other functions
def get_token_id(token_address):
    token_id = -1

    if token_address == '0x37FA438EdfB7044E9444b4022b2516C4dAA4592F':
        token_id = 0
    
    elif token_address == '0x18bA3e87876f4982810d321D447b81d01Cdf6668':
        token_id = 1
    
    elif token_address == '0x475f3ab387157ebc645874aea1836223b7cc5d19':
        token_id = 2

    elif token_address == '0x73d49aC28C4Fea2B8e7C6BF45d64A2e68ed53bE0':
        token_id = 3
    
    elif token_address == '0x7f5eC43a46dF54471DAe95d3C05BEBe7301b75Ff':
        token_id = 4
    
    return token_id

# # gets out token symbols
def get_token_symbol(token_id):
    
    token_symbol_list = ['USDC', 'USDT', 'WBTC', 'WETH', 'METIS']

    token_symbol = token_symbol_list[token_id]
    
    return token_symbol

# # accounts for out token decimals
def get_clean_token_amount(token_id, token_volume):

    decimal_list = [1e6, 1e6, 1e8, 1e18, 1e18]

    token_amount = token_volume / decimal_list[token_id]

    return token_amount

#makes a dataframe and stores it in a csv file
def make_user_data_csv(df):
    old_df = pd.read_csv('all_events.csv')
    old_df = old_df.drop_duplicates(subset=['tx_hash', 'token_address', 'token_amount'], keep='last')

    combined_df_list = [df, old_df]
    combined_df = pd.concat(combined_df_list)
    combined_df = combined_df.drop_duplicates(subset=['tx_hash', 'token_address', 'token_amount'], keep='last')

    # combined_df = make_checksum_values(combined_df)

    if len(combined_df) >= len(old_df):
        combined_df.to_csv('all_events.csv', index=False)
        print('Event CSV Updated')
    return

#makes a dataframe and stores it in a csv file
def make_lge_data_csv(df):
    old_df = pd.read_csv('grain_remaining_vests.csv')
    old_df = old_df.drop_duplicates(subset=['wallet_address','remaining_vest','chain'], keep='last')

    combined_df_list = [df, old_df]
    combined_df = pd.concat(combined_df_list)
    combined_df = combined_df.drop_duplicates(subset=['wallet_address','remaining_vest','chain'], keep='last')

    if len(combined_df) >= len(old_df):
        combined_df.to_csv('grain_remaining_vests.csv', index=False)
        print('Event CSV Updated')
    return

# # takes in an a_token address and returns it's contract object
def get_token_contract(contract_address, web3):
    contract_abi = [{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"index","type":"uint256"}],"name":"BalanceTransfer","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"target","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"index","type":"uint256"}],"name":"Burn","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"underlyingAsset","type":"address"},{"indexed":True,"internalType":"address","name":"pool","type":"address"},{"indexed":False,"internalType":"address","name":"treasury","type":"address"},{"indexed":False,"internalType":"address","name":"incentivesController","type":"address"},{"indexed":False,"internalType":"uint8","name":"aTokenDecimals","type":"uint8"},{"indexed":False,"internalType":"string","name":"aTokenName","type":"string"},{"indexed":False,"internalType":"string","name":"aTokenSymbol","type":"string"},{"indexed":False,"internalType":"bytes","name":"params","type":"bytes"}],"name":"Initialized","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"index","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"ATOKEN_REVISION","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"EIP712_REVISION","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"POOL","outputs":[{"internalType":"contract ILendingPool","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"RESERVE_TREASURY_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"UNDERLYING_ASSET_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"_nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"address","name":"receiverOfUnderlying","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getIncentivesController","outputs":[{"internalType":"contract IAaveIncentivesController","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getScaledUserBalanceAndSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"handleRepayment","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract ILendingPool","name":"pool","type":"address"},{"internalType":"address","name":"treasury","type":"address"},{"internalType":"address","name":"underlyingAsset","type":"address"},{"internalType":"contract IAaveIncentivesController","name":"incentivesController","type":"address"},{"internalType":"uint8","name":"aTokenDecimals","type":"uint8"},{"internalType":"string","name":"aTokenName","type":"string"},{"internalType":"string","name":"aTokenSymbol","type":"string"},{"internalType":"bytes","name":"params","type":"bytes"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"mint","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"mintToTreasury","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"scaledBalanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"scaledTotalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferOnLiquidation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"target","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferUnderlyingTo","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"}]    
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    return contract

# # takes in a contract object and returns all associated transfer events
def get_transfer_events(contract, from_block, to_block):

    events = contract.events.Transfer.get_logs(fromBlock=from_block, toBlock=to_block)
    
    return events

#returns a df if a tx_hash exists
def chain_exists(df, chain):

    new_df = pd.DataFrame()

    if ((df['chain'] == chain)).any():
        new_df = df.loc[df['chain'] == chain]
    
    return new_df

#returns df if wallet_address exists
def wallet_address_exists(df, wallet_address):

    if ((df['wallet_address'] == wallet_address)).any():
        df = df.loc[df['wallet_address'] == wallet_address]

    else:
        df = pd.DataFrame()

    return df

# will tell us whether we need to find new data
# returns a boolean
def already_part_of_df(chain, wallet_address):

    all_exist = False

    df = pd.read_csv('grain_remaining_vests.csv')

    new_df = wallet_address_exists(df, wallet_address)

    if len(new_df) > 0:
        new_df = chain_exists(new_df, chain)

        if len(new_df) > 0:
            all_exist = True

    return all_exist

#makes our dataframe
def user_data(events, web3):
    
    df = pd.DataFrame()

    tx_hash_list = []
    from_list = []
    to_list = []
    timestamp_list = []
    token_address_list = []
    token_symbol_list = []
    token_amount_list = []
    block_list = []

    user = ''

    start_time = time.time()
    i = 1
    for event in events:

        counter = 0
        print('Batch of Events Processed: ', i, '/', len(events))
        i+=1

        to_address = event['args']['to']


        if to_address == '0x9DD07fF57C0e9cA6D2009911bEE273106fe0DAf7':
            counter += 2

        if counter == 2:
            time.sleep(0.1)

            tx_hash = event['transactionHash'].hex()
            tx_hash_list.append(tx_hash)
            from_address = event['args']['from']
            from_list.append(from_address)
            to_list.append(to_address)

            block = web3.eth.get_block(event['blockNumber'])
            block_number = int(block['number'])

            if int(block_number) == 5190033:
                print(event)
            block_list.append(block_number)

            timestamp_list.append(block['timestamp'])
            token_address = event['address']
            token_address_list.append(token_address)
            
            token_id = get_token_id(token_address)

            token_symbol = get_token_symbol(token_id)
            token_symbol_list.append(token_symbol)
            token_volume = event['args']['value']

            token_amount = get_clean_token_amount(token_id, token_volume)
            token_amount_list.append(token_amount)

    df['tx_hash'] = tx_hash_list
    df['from_address'] = from_list
    df['to_address'] = to_list
    df['timestamp'] = timestamp_list
    df['token_address'] = token_address_list
    df['token_symbol'] = token_symbol_list
    df['token_amount'] = token_amount_list
    df['block_number'] = block_list

    return df

# # will find all the transfer events for a token given a certain chain's rpc
def find_chain_transactions(rpc_url, token_list, latest_block, from_block, interval):

    to_block = from_block + interval

    web3 = get_web_3(rpc_url)

    contract_list = [get_token_contract(token, web3) for token in token_list]

    while to_block < latest_block:
        print('Current Event Block vs Latest Event Block to Check: ', from_block, '/', latest_block, 'Blocks Remaining: ', latest_block - from_block)

        for contract in contract_list:

            transfer_events = get_transfer_events(contract, from_block, to_block)
            if len(transfer_events) > 0:
                transfer_df = user_data(transfer_events, web3)
                make_user_data_csv(transfer_df)
            time.sleep(1)
        
        # increments our block ranges
        from_block += interval
        to_block += interval

        time.sleep(.25)

        if from_block >= latest_block:
            from_block = latest_block - 1
        
        if to_block >= latest_block:
            to_block = latest_block

    return transfer_df

# # runs all our looks
# # updates our csv
def find_all_transactions():
    
    chain_index = 3

    while chain_index < 7:
        chain_info_list = get_chain_info(chain_index)
        rpc_url_list = chain_info_list[0]
        rpc_url = rpc_url_list[0]
        token_list = get_token_list(chain_index)
        to_block = get_lge_to_block(chain_index)
        from_block = get_lge_from_block(chain_index)
        interval = get_interval(chain_index)

        find_chain_transactions(rpc_url, token_list, to_block, from_block, interval)

        chain_index += 1

    # token_list = ["0xEA32A96608495e54156Ae48931A7c20f0dcc1a21", "0xDeadDeAddeAddEAddeadDEaDDEAdDeaDDeAD0000", "0xbB06DCA3AE6887fAbF931640f67cab3e3a16F4dC", "0x420000000000000000000000000000000000000A"]

    # latest_block = 5221891
    # from_block = 5109933

    # # latest_block = web3.eth.get_block('latest')
    # # latest_block = int(latest_block['number'])

    # # event_df = pd.read_csv('all_events.csv')

    # # try:
    # #     from_block = int(max(event_df['block_number']))
    # # except:
    # #     from_block = FROM_BLOCK

    # # from_block = FROM_BLOCK
    
    # # from_block = 2869000

    # interval = 20000

    # # to_block = from_block + 955
    # to_block = from_block + interval

    # contract_list = [get_token_contract(token) for token in token_list]

    # while to_block < latest_block:
    #     print('Current Event Block vs Latest Event Block to Check: ', from_block, '/', latest_block, 'Blocks Remaining: ', latest_block - from_block)

    #     for contract in contract_list:

    #         transfer_events = get_transfer_events(contract, from_block, to_block)
    #         if len(transfer_events) > 0:
    #             transfer_df = user_data(transfer_events)
    #             make_user_data_csv(transfer_df)
    #         time.sleep(1)
    #     from_block += interval
    #     to_block += interval

    #     time.sleep(.25)

    #     if from_block >= latest_block:
    #         from_block = latest_block - 1
        
    #     if to_block >= latest_block:
    #         to_block = latest_block
    
    return transfer_df

# # Makes a day column that is the same as used in dune
def format_df_timestamp(csv_name):
    df = pd.read_csv(csv_name)

    df['day'] = pd.to_datetime(df['timestamp'], unit='s').dt.tz_localize(None)

    df['day'] = df['day'].dt.strftime('%Y-%m-%d %H:%M')

    df['day'] = df['day'].astype(str)

    df.to_csv(csv_name, index=False)
    return

# # finds the unique wallet addresses from our transactions
def find_unique_wallet_addresses(csv_name, chain_name):

    df = pd.read_csv(csv_name)
    print(df)

    unique_wallet_list = df.from_address.unique()

    new_df = pd.DataFrame()

    new_df['wallet_address'] = unique_wallet_list
    new_df['chain'] = 'METIS'

    lge_df = pd.read_csv('grain_lge_wallets.csv')

    df_list = [new_df, lge_df]

    combined_df = pd.concat(df_list)

    print(combined_df)

    combined_df.to_csv('grain_lge_wallets.csv', index=False)
    return

def get_ui_data_provider_contract(contract_address, web3):
    contract_abi =  [{"inputs":[{"internalType":"address","name":"_lge","type":"address"},{"internalType":"address","name":"_grainSaleClaim","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"MAX_KINK_RELEASES","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MAX_RELEASES","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PERCENT_DIVISOR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PERIOD","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getNumberOfReleases","outputs":[{"internalType":"uint256","name":"numberOfReleases","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getPending","outputs":[{"internalType":"uint256","name":"claimable","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getTotalClaimed","outputs":[{"internalType":"uint256","name":"totalClaimed","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getTotalOwed","outputs":[{"internalType":"uint256","name":"userTotal","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getUserData","outputs":[{"components":[{"internalType":"uint256","name":"numberOfReleases","type":"uint256"},{"internalType":"uint256","name":"totalOwed","type":"uint256"},{"internalType":"uint256","name":"pending","type":"uint256"},{"internalType":"uint256","name":"totalClaimed","type":"uint256"},{"internalType":"uint256","name":"userGrainLeft","type":"uint256"}],"internalType":"struct UiDataProvider.UserData","name":"userData","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getUserGrainLeft","outputs":[{"internalType":"uint256","name":"grainLeft","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getUserTotalWeight","outputs":[{"internalType":"uint256","name":"totalWeight","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"grainSaleClaim","outputs":[{"internalType":"contract IGrainSaleClaim","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lge","outputs":[{"internalType":"contract IGrainLGE","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxDiscount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxKinkDiscount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    
    return contract

# # finds the remaining vest amount for a given contract and wallet address
def find_vest_amount(contract, wallet_address, wait_time):
    
    vest_amount = contract.functions.getUserGrainLeft(wallet_address).call()
    
    time.sleep(wait_time)

    vest_amount = vest_amount / 1e18

    return vest_amount


def get_chain_info(chain_index):

    ftm_rpc_list = ['https://rpcapi.fantom.network', 'https://rpc.ftm.tools', 'https://fantom-pokt.nodies.app', 'https://fantom.drpc.org', 'https://fantom.drpc.org']
    matic_rpc_list = ['https://rpc-mainnet.matic.quiknode.pro']
    optimism_rpc_list = ['https://optimism.gateway.tenderly.co']
    metis_rpc_list = ['https://andromeda.metis.io', 'https://metis-pokt.nodies.app']
    arbitrum_rpc_list = ['https://arb-mainnet-public.unifra.io']
    bsc_rpc_list = ['https://public.stackup.sh/api/v1/node/bsc-mainnet']
    eth_rpc_list = ['https://eth-pokt.nodies.app']

    rpc_combined_list = [ftm_rpc_list, matic_rpc_list, optimism_rpc_list, metis_rpc_list, arbitrum_rpc_list, bsc_rpc_list, eth_rpc_list]
    chain_list = ['FTM', 'MATIC', 'OP', 'METIS', 'ARB', 'BNB', 'ETH']
    token_contract_list = ['0x02838746d9E1413E07EE064fcBada57055417f21', '0x8429d0AFade80498EAdb9919E41437A14d45A00B', '0xfD389Dc9533717239856190F42475d3f263a270d', '0xE1537feF008944D1c8DcAfBAcE4DC76D31D22DC5', '0x80bB30D62a16e1F2084dEAE84dc293531c3AC3A1', '0x8F87A7d376821c7B2658a005aAf190Ec778BF37A', '0xF88Baf18FAB7e330fa0C4F83949E23F52FECECce']
    grain_sale_claim_list = ['0x99f7f1A1dD30457dFaD312b4064Fa4Ad4B73B2d7', '0x99f7f1A1dD30457dFaD312b4064Fa4Ad4B73B2d7', '0x99f7f1A1dD30457dFaD312b4064Fa4Ad4B73B2d7', '0x99f7f1A1dD30457dFaD312b4064Fa4Ad4B73B2d7', '0x99f7f1A1dD30457dFaD312b4064Fa4Ad4B73B2d7', '0x99f7f1A1dD30457dFaD312b4064Fa4Ad4B73B2d7', '0x99f7f1A1dD30457dFaD312b4064Fa4Ad4B73B2d7']
    ui_data_provider_list = ['0x9f123572F1488C9Ab8b39baca8285BDeABdeDb7e']

    chain_info_list = [rpc_combined_list[chain_index], chain_list[chain_index], token_contract_list[chain_index], grain_sale_claim_list[chain_index], ui_data_provider_list[0]]

    return chain_info_list

# # gets our to block
def get_lge_to_block(chain_index):
    chain_list = ['FTM', 'MATIC', 'OP', 'METIS', 'ARB', 'BNB', 'ETH']

    to_block_list = [58881393, 41035952, 85523772, 5221891, 76172561, 26984331, 16957713]

    to_block = to_block_list[chain_index]

    return to_block

# # gets our from block
def get_lge_from_block(chain_index):
    chain_list = ['FTM', 'MATIC', 'OP', 'METIS', 'ARB', 'BNB', 'ETH']
    from_block_list = [57841624, 40486218, 81872542, 5110013, 71059329, 26569086, 16854057]

    from_block = from_block_list[chain_index]

    return from_block

# # returns a nested list of our tokens
def get_token_list(chain_index):
    combined_token_list = []
    
    ftm_token_list = ['-1']
    matic_token_list = ['-1']
    op_token_list = ['-1']
    metis_token_list = ["0xEA32A96608495e54156Ae48931A7c20f0dcc1a21", "0xDeadDeAddeAddEAddeadDEaDDEAdDeaDDeAD0000", "0xbB06DCA3AE6887fAbF931640f67cab3e3a16F4dC", "0x420000000000000000000000000000000000000A"]
    arb_token_list = ['-1']
    bnb_token_list = ['-1']
    eth_token_list = ['-1']

    combined_token_list = [ftm_token_list, matic_token_list, op_token_list, metis_token_list, arb_token_list, bnb_token_list, eth_token_list]

    return combined_token_list[chain_index]

# # returns the interval we can use for a blockchain
def get_interval(chain_index):
    chain_list = ['FTM', 'MATIC', 'OP', 'METIS', 'ARB', 'BNB', 'ETH']
    interval_list = [5000, 5000, 5000, 20000, 2500, 5000, 5000]

    return interval_list[chain_index]

# # will loop through one RPC iteration
def loop_through_rpc(df, ui_data_provider_contract, wait_time, grain_to_claim):

    wallet_address_list = df['wallet_address'].to_list()
    wallet_address_list = [Web3.to_checksum_address(x) for x in wallet_address_list]

    chain = df['chain'].iloc[0]

    wallet_vest_list = []
    remaining_vest_amount_list = []

    chain_df = pd.DataFrame()

    # strictly to find out how much grain has already been found
    lge_df = pd.read_csv('grain_remaining_vests.csv')
    lge_df = lge_df.loc[lge_df['chain'] == chain]
    amount_of_found_grain = lge_df['remaining_vest'].sum()

    wallets_checked = 0

    # # iterates through every wallet on a specific chain
    for wallet_address in wallet_address_list:

        exists = already_part_of_df(chain, wallet_address)

        if exists == False:

            remaining_vest_amount = find_vest_amount(ui_data_provider_contract, wallet_address, wait_time)

            if remaining_vest_amount > 0:
                wallet_vest_list.append(wallet_address)
                remaining_vest_amount_list.append(remaining_vest_amount)
                amount_of_found_grain += remaining_vest_amount

        print(wallets_checked, ' / ', len(wallet_address_list), ' ', chain , ' Wallets Remaining: ', len(wallet_address_list) - wallets_checked, ' Grain Remaining to Find: ', grain_to_claim - amount_of_found_grain)
        wallets_checked += 1

    print(chain, ' Chain Complete')
    chain_df['wallet_address'] = wallet_vest_list
    chain_df['remaining_vest'] = remaining_vest_amount_list
    chain_df['chain'] = chain
    make_lge_data_csv(chain_df)

    grain_found = chain_df['remaining_vest'].sum()
    
    
    return grain_found

# # mmakes our web3 object and injects it's middleware
def get_web_3(rpc_url):
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    time.sleep(2.5)
    print('Web3: ', web3)
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    time.sleep(2.5)
    
    return web3

def find_single_rpc_vests(lge_csv, chain, token_contract, ui_data_provider_contract_address, wait_time, total_grain_to_claim):

    lge_df = pd.read_csv(lge_csv)
    df = lge_df.loc[lge_df['chain'] == chain]
    
    web3 = get_web_3(rpc_url)

    token_contract = get_token_contract(token_contract, web3)

    ui_data_provider_contract = get_ui_data_provider_contract(ui_data_provider_contract_address, web3)

    grain_found = loop_through_rpc(df, ui_data_provider_contract, wait_time, total_grain_to_claim)

    return grain_found

# # finds the total grain of a chain
# # then runs through different RPCs for that chain to try to find all grain
def find_chains_vested_grain(chain_index, lge_csv):
    
    chain_info_list = get_chain_info(chain_index)

    rpc_url_list = chain_info_list[0]
    chain_symbol = chain_info_list[1]
    token_contract = chain_info_list[2]
    grain_sale_claim_contract_address = chain_info_list[3]
    ui_data_provider_contract_address = chain_info_list[4]

    total_grain_to_claim = -1
    grain_found = 0
    
    need_to_find_more_grain = True

    wait_time = 1.5
    i = 0

    while i < len(rpc_url_list):

        
        total_grain_to_claim = find_claim_total(token_contract, grain_sale_claim_contract_address)

        grain_found += find_single_rpc_vests(lge_csv, chain_symbol, token_contract, ui_data_provider_contract_address, wait_time, total_grain_to_claim)

        if grain_found > total_grain_to_claim - 100:
            print(grain_found, ' / ', total_grain_to_claim, ' Grain Found. Grain Remaining:', total_grain_to_claim - grain_found)
            print('Looping through the next RPC')
            time.sleep(2)
            need_to_find_more_grain = False

        if need_to_find_more_grain == True:
            i += 1
        else:
            break
        

        

    return

# # will loop through each chain to look for wallet vest amounts
def make_vest_df():

    chain_list = ['FTM', 'MATIC', 'OP', 'METIS', 'ARB', 'BNB', 'ETH']

    lge_csv = 'grain_lge_wallets.csv'

    i = 0

    # # iterates through each chain
    while i < len(chain_list):

        find_chains_vested_grain(i, lge_csv)

    
        i += 1

    return


# # returns how much grain there is to be claimed
def find_claim_total(contract, wallet_address):

    grain_amount = contract.functions.balanceOf(wallet_address).call()

    grain_amount = grain_amount / 1e18

    return grain_amount

# contract = get_token_contract('0xfD389Dc9533717239856190F42475d3f263a270d')

# total_claim_amount = find_claim_total(contract, '0x99f7f1A1dD30457dFaD312b4064Fa4Ad4B73B2d7')

# print(total_claim_amount)

find_all_transactions()

# csv_name = 'all_events.csv'

# find_unique_wallet_addresses(csv_name, 'METIS')

# format_df_timestamp(csv_name)

# make_vest_df()

# contract_address = '0x9f123572F1488C9Ab8b39baca8285BDeABdeDb7e'

# contract = get_ui_data_provider_contract(contract_address)

# find_vest_amount(contract, wallet_address)

# vest_df = pd.read_csv('grain_remaining_vests.csv')

# vest_df = vest_df.loc[vest_df['chain'] == 'OP']

# print(vest_df['remaining_vest'].sum())