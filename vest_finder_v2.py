from web3 import Web3
from web3.middleware import geth_poa_middleware 
import pandas as pd
import time

CHAIN_INDEX = 0

WAIT_TIME = 0.75

# # mmakes our web3 object and injects it's middleware
def get_web_3(rpc_url):

    if 'wss' in rpc_url:
        provider = Web3.WebsocketProvider(rpc_url)
        web3 = Web3(provider)
    else:
        web3 = Web3(Web3.HTTPProvider(rpc_url))
    time.sleep(2.5)
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    time.sleep(2.5)
    
    return web3

# # gets our chain's rpc list
def get_rpc_list(chain_index):
    # ftm_rpc_list = ['https://rpcapi.fantom.network', 'https://rpc.ftm.tools', 'https://fantom-pokt.nodies.app', 'https://fantom.drpc.org', 'https://fantom.drpc.org', 'https://twilight-green-season.fantom.quiknode.pro']
    # ftm_rpc_list = ['wss://fantom-rpc.publicnode.com']
    ftm_rpc_list = ['https://rpc.ftm.tools']
    matic_rpc_list = ['https://polygon.llamarpc.com']
    optimism_rpc_list = ['https://rpc.ankr.com/optimism']
    metis_rpc_list = ['https://andromeda.metis.io'] # # **
    arbitrum_rpc_list = ['https://arbitrum.llamarpc.com']
    bsc_rpc_list = ['https://binance.llamarpc.com']
    # eth_rpc_list = ['https://eth-pokt.nodies.app']
    eth_rpc_list = ['https://eth.llamarpc.com']

    rpc_combined_list = [ftm_rpc_list, matic_rpc_list, optimism_rpc_list, metis_rpc_list, arbitrum_rpc_list, bsc_rpc_list, eth_rpc_list]

    return rpc_combined_list[chain_index]

# # gets our chain's gas token symbol
def get_chain_symbol(chain_index):
    chain_list = ['FTM', 'MATIC', 'OP', 'METIS', 'ARB', 'BNB', 'ETH']

    return chain_list[chain_index]

# # gets our chain's grain contract address
def get_grain_contract_address(chain_index):
    grain_token_list = ['0x02838746d9E1413E07EE064fcBada57055417f21', '0x8429d0AFade80498EAdb9919E41437A14d45A00B', '0xfD389Dc9533717239856190F42475d3f263a270d', '0xE1537feF008944D1c8DcAfBAcE4DC76D31D22DC5', '0x80bB30D62a16e1F2084dEAE84dc293531c3AC3A1', '0x8F87A7d376821c7B2658a005aAf190Ec778BF37A', '0xF88Baf18FAB7e330fa0C4F83949E23F52FECECce']
   
    return grain_token_list[chain_index]

# # gets our chain's grain claim contract address
def get_grain_claim_contract_address(chain_index):
    grain_claim_list = [Web3.to_checksum_address('0x99f7f1A1dD30457dFaD312b4064Fa4Ad4B73B2d7')]

    return grain_claim_list[0]


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

# # gets as the ui_data_provider_contract_address
def get_ui_data_provider_contract_address(chain_index):
    ui_data_provider_contract_address_list = ['0x9f123572F1488C9Ab8b39baca8285BDeABdeDb7e']

    return ui_data_provider_contract_address_list[0]

# # takes in an a_token address and returns it's contract object
def get_token_contract(contract_address, web3):
    contract_abi = [{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"index","type":"uint256"}],"name":"BalanceTransfer","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"target","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"index","type":"uint256"}],"name":"Burn","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"underlyingAsset","type":"address"},{"indexed":True,"internalType":"address","name":"pool","type":"address"},{"indexed":False,"internalType":"address","name":"treasury","type":"address"},{"indexed":False,"internalType":"address","name":"incentivesController","type":"address"},{"indexed":False,"internalType":"uint8","name":"aTokenDecimals","type":"uint8"},{"indexed":False,"internalType":"string","name":"aTokenName","type":"string"},{"indexed":False,"internalType":"string","name":"aTokenSymbol","type":"string"},{"indexed":False,"internalType":"bytes","name":"params","type":"bytes"}],"name":"Initialized","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"index","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"ATOKEN_REVISION","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"EIP712_REVISION","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"POOL","outputs":[{"internalType":"contract ILendingPool","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"RESERVE_TREASURY_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"UNDERLYING_ASSET_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"_nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"address","name":"receiverOfUnderlying","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getIncentivesController","outputs":[{"internalType":"contract IAaveIncentivesController","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getScaledUserBalanceAndSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"handleRepayment","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract ILendingPool","name":"pool","type":"address"},{"internalType":"address","name":"treasury","type":"address"},{"internalType":"address","name":"underlyingAsset","type":"address"},{"internalType":"contract IAaveIncentivesController","name":"incentivesController","type":"address"},{"internalType":"uint8","name":"aTokenDecimals","type":"uint8"},{"internalType":"string","name":"aTokenName","type":"string"},{"internalType":"string","name":"aTokenSymbol","type":"string"},{"internalType":"bytes","name":"params","type":"bytes"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"mint","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"mintToTreasury","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"scaledBalanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"scaledTotalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferOnLiquidation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"target","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferUnderlyingTo","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"}]    
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    return contract

# # does as the name implies
def get_grain_sale_claim_abi():

    abi = [{"inputs":[{"internalType":"address","name":"_lge","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"GrainSaleClaim__GrainAlreadySet","type":"error"},{"inputs":[],"name":"GrainSaleClaim__GrainNotSet","type":"error"},{"inputs":[],"name":"GrainSaleClaim__WeightAlreadySet","type":"error"},{"inputs":[],"name":"GrainSaleClaim__WeightNotSet","type":"error"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"user","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Claim","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"inputs":[],"name":"MAX_KINK_RELEASES","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MAX_RELEASES","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PERCENT_DIVISOR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PERIOD","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"claim","outputs":[{"internalType":"uint256","name":"claimable","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"cumulativeWeight","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getUserShares","outputs":[{"internalType":"uint256","name":"userTotalWeight","type":"uint256"},{"internalType":"uint256","name":"numberOfReleases","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"grain","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lge","outputs":[{"internalType":"contract IGrainLGE","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lgeEnd","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxDiscount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxKinkDiscount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_cumulativeWeight","type":"uint256"}],"name":"setCumulativeWeight","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"grainAmount","type":"uint256"}],"name":"setTotalChainShare","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"totalGrain","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userShares","outputs":[{"internalType":"uint256","name":"userTotalWeight","type":"uint256"},{"internalType":"uint256","name":"numberOfReleases","type":"uint256"},{"internalType":"uint256","name":"totalClaimed","type":"uint256"}],"stateMutability":"view","type":"function"}]

    return abi

# # gets our contract object
def get_grain_sale_claim_contract(web3, contract_address):

    abi = get_grain_sale_claim_abi()

    contract = web3.eth.contract(address=contract_address, abi=abi)

    return contract

# # calls the user_shares function
# # returns a neatly formatted dataframe
def get_user_shares(contract, wallet_address):

    df = pd.DataFrame()

    user_share_data = contract.functions.userShares(wallet_address).call()

    user_total_weight = user_share_data[0]
    number_of_releases = user_share_data[1]
    total_claimed = user_share_data[2]

    df['wallet_address'] = [wallet_address]
    df['user_total_weight'] = [user_total_weight]
    df['number_of_releases'] = [number_of_releases]
    df['total_claimed'] = [total_claimed]

    return  df

# # calls the get_user_shares function
# # returns a neatly formatted dataframe
def get_get_user_shares(contract, wallet_address):

    df = pd.DataFrame()

    user_share_data = contract.functions.getUserShares(wallet_address).call()

    user_total_weight = user_share_data[0]
    number_of_releases = user_share_data[1]
    total_claimed = 0

    df['wallet_address'] = [wallet_address]
    df['user_total_weight'] = [user_total_weight]
    df['number_of_releases'] = [number_of_releases]
    df['total_claimed'] = [total_claimed]

    return df

# # tells us the exchange ratio between grain to weight
def get_grain_to_weight(contract):

    cumulative_weight = float(contract.functions.cumulativeWeight().call())
    total_grain = float(contract.functions.totalGrain().call())

    grain_to_weight = total_grain / cumulative_weight

    return grain_to_weight

def run_all(chain_index):

    wallet_address_df = pd.read_csv('dune_wallet_addresses.csv')
    contract_address = get_grain_claim_contract_address(chain_index)
    rpc_list = get_rpc_list(chain_index)
    chain = get_chain_symbol(chain_index)

    unique_wallet_address_list = wallet_address_df['wallet_address'].unique()
    unique_wallet_address_list = [Web3.to_checksum_address(x) for x in unique_wallet_address_list]

    df_list = []

    for rpc_url in rpc_list:
        rpc_url = rpc_list[0]
        web3 = get_web_3(rpc_url)
        contract = get_grain_sale_claim_contract(web3, contract_address)

        i = 1
        for wallet_address in unique_wallet_address_list:
            
            # # adds a timeout handler
            try:
                df = get_user_shares(contract, wallet_address)
            except:
                time.sleep(30)
                df = get_user_shares(contract, wallet_address)

            time.sleep(WAIT_TIME)

            if df['user_total_weight'].iloc[0] == 0:
                
                # # adds a timeout handler
                try:
                    df = get_get_user_shares(contract, wallet_address)
                except:
                    time.sleep(30)
                    df = get_get_user_shares(contract, wallet_address)

                print(df)

                time.sleep(WAIT_TIME)


            if len(df) > 0:
                df['chain'] = [chain]
                df_list.append(df)
            
            print('Wallets Checked: ', len(unique_wallet_address_list), '/', i, 'Remaining: ', len(unique_wallet_address_list)-i)
            i+= 1

    df = pd.concat(df_list)

    return df

# chain_index = 5
# df = run_all(chain_index)
# df.to_csv('grain_claim_test.csv',index=False)

df = pd.read_csv('dune_wallet_addresses.csv')
df = df.drop_duplicates(subset=['wallet_address'])
df.to_csv('dune_wallet_addresses.csv', index=False)

# df_1 = pd.read_csv('gct_1.csv')
# df_2 = pd.read_csv('gct_2.csv')
# # df_3 = pd.read_csv('gct_3.csv')
# # df_4 = pd.read_csv('gct_4.csv')

# df = pd.concat([df_1, df_2])
# df = df.drop_duplicates(subset=['wallet_address', 'user_total_weight', 'number_of_releases', 'total_claimed', 'chain'])
# # df = df.drop_duplicates(subset=['wallet_address'])
# print(df)
# print(df['user_total_weight'].sum())

# df.to_csv('test_test.csv', index=False)