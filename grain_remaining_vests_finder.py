from web3 import Web3
from web3.middleware import geth_poa_middleware 
import pandas as pd
import time

# # mmakes our web3 object and injects it's middleware
def get_web_3(rpc_url):
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    time.sleep(2.5)
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    time.sleep(2.5)
    
    return web3

# # gets our chain's rpc list
def get_rpc_list(chain_index):
    ftm_rpc_list = ['https://rpcapi.fantom.network', 'https://rpc.ftm.tools', 'https://fantom-pokt.nodies.app', 'https://fantom.drpc.org', 'https://fantom.drpc.org']
    matic_rpc_list = ['https://rpc-mainnet.matic.quiknode.pro']
    optimism_rpc_list = ['https://optimism.gateway.tenderly.co']
    metis_rpc_list = ['https://andromeda.metis.io', 'https://metis-pokt.nodies.app']
    arbitrum_rpc_list = ['https://arb-mainnet-public.unifra.io']
    bsc_rpc_list = ['https://public.stackup.sh/api/v1/node/bsc-mainnet']
    eth_rpc_list = ['https://eth-pokt.nodies.app']

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
    grain_claim_list = ['0x99f7f1A1dD30457dFaD312b4064Fa4Ad4B73B2d7']

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

# # returns how much grain there is to be claimed
def find_claim_total(contract, wallet_address):

    grain_amount = contract.functions.balanceOf(wallet_address).call()

    grain_amount = grain_amount / 1e18

    return grain_amount

def get_ui_data_provider_contract(contract_address, web3):
    contract_abi =  [{"inputs":[{"internalType":"address","name":"_lge","type":"address"},{"internalType":"address","name":"_grainSaleClaim","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"MAX_KINK_RELEASES","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MAX_RELEASES","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PERCENT_DIVISOR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PERIOD","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getNumberOfReleases","outputs":[{"internalType":"uint256","name":"numberOfReleases","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getPending","outputs":[{"internalType":"uint256","name":"claimable","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getTotalClaimed","outputs":[{"internalType":"uint256","name":"totalClaimed","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getTotalOwed","outputs":[{"internalType":"uint256","name":"userTotal","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getUserData","outputs":[{"components":[{"internalType":"uint256","name":"numberOfReleases","type":"uint256"},{"internalType":"uint256","name":"totalOwed","type":"uint256"},{"internalType":"uint256","name":"pending","type":"uint256"},{"internalType":"uint256","name":"totalClaimed","type":"uint256"},{"internalType":"uint256","name":"userGrainLeft","type":"uint256"}],"internalType":"struct UiDataProvider.UserData","name":"userData","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getUserGrainLeft","outputs":[{"internalType":"uint256","name":"grainLeft","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getUserTotalWeight","outputs":[{"internalType":"uint256","name":"totalWeight","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"grainSaleClaim","outputs":[{"internalType":"contract IGrainSaleClaim","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lge","outputs":[{"internalType":"contract IGrainLGE","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxDiscount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxKinkDiscount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    
    return contract

#returns df if wallet_address exists
def wallet_address_exists(df, wallet_address):

    if ((df['wallet_address'] == wallet_address)).any():
        df = df.loc[df['wallet_address'] == wallet_address]

    else:
        df = pd.DataFrame()

    return df

#returns a df if a tx_hash exists
def chain_exists(df, chain):

    new_df = pd.DataFrame()

    if ((df['chain'] == chain)).any():
        new_df = df.loc[df['chain'] == chain]
    
    return new_df

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

# # finds the remaining vest amount for a given contract and wallet address
def find_vest_amount(contract, wallet_address, wait_time):
    
    vest_amount = contract.functions.getUserGrainLeft(wallet_address).call()
    
    time.sleep(wait_time)

    vest_amount = vest_amount / 1e18

    return vest_amount

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
    print(lge_df)
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

# # finds all the vests using a single rpc
def find_single_rpc_vests(lge_csv, chain, ui_data_provider_contract_address, wait_time, total_grain_to_claim, rpc_url):

    print(ui_data_provider_contract_address)
    lge_df = pd.read_csv(lge_csv)
    df = lge_df.loc[lge_df['chain'] == chain]
    
    web3 = get_web_3(rpc_url)

    ui_data_provider_contract = get_ui_data_provider_contract(ui_data_provider_contract_address, web3)

    grain_found = loop_through_rpc(df, ui_data_provider_contract, wait_time, total_grain_to_claim)

    return grain_found

# # finds the total grain of a chain
# # then runs through different RPCs for that chain to try to find all grain
def find_chains_vested_grain(chain_index, lge_csv):

    rpc_url_list = get_rpc_list(chain_index)
    chain_symbol = get_chain_symbol(chain_index)
    grain_contract_address = get_grain_contract_address(chain_index)
    grain_sale_claim_contract_address = get_grain_claim_contract_address(chain_index)
    ui_data_provider_contract_address = get_ui_data_provider_contract_address(chain_index)

    rpc_url = rpc_url_list[0]
    web3 = get_web_3(rpc_url)
    grain_token_contract = get_token_contract(grain_contract_address, web3)

    total_grain_to_claim = find_claim_total(grain_token_contract, grain_sale_claim_contract_address)

    # total_grain_to_claim = -1
    grain_found = 0
    
    need_to_find_more_grain = True

    wait_time = 1.5
    i = 0

    while i < len(rpc_url_list):
        rpc_url = rpc_url_list[i]

        grain_found += find_single_rpc_vests(lge_csv, chain_symbol, ui_data_provider_contract_address, wait_time, total_grain_to_claim, rpc_url)

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

    i = 3

    # # iterates through each chain
    while i < len(chain_list):

        find_chains_vested_grain(i, lge_csv)

    
        i += 1

    return

make_vest_df()