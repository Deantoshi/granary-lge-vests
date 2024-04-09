from web3 import Web3
from web3.middleware import geth_poa_middleware 
import pandas as pd
import time

# # essentially gets our web3 rpc connection
def get_web_3():
    rpc_url = 'wss://fantom-rpc.publicnode.com'
    provider = Web3.WebsocketProvider(rpc_url)
    web3 = Web3(provider)
    time.sleep(2.5)
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    time.sleep(2.5)

    return web3

# # reads our csv into a dataframe object
# # drops duplicates buyer addresses from the dataframe
# # turns our unique buyer addresses into their checksum forms
# # returns dataframe
def get_oath_lge_buyers_df(csv_name):
    df = pd.read_csv(csv_name)
    df = df.drop_duplicates(subset=['buyer_address'])

    buyer_address_list = df['buyer_address'].to_list()

    checksum_buyer_address_list = [Web3.to_checksum_address(x) for x in buyer_address_list]

    df['buyer_address'] = checksum_buyer_address_list

    return df

def get_oath_lge_abi():
    contract_abi = [{"inputs":[{"internalType":"address","name":"_oath","type":"address"},{"internalType":"address","name":"_counterAsset","type":"address"},{"internalType":"uint256","name":"_totalOath","type":"uint256"},{"internalType":"uint256","name":"_beginning","type":"uint256"},{"internalType":"uint256","name":"_end","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"inputs":[],"name":"BASIS_POINTS","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"addr","type":"address"},{"internalType":"uint256","name":"threshold","type":"uint256"},{"internalType":"uint256","name":"limit","type":"uint256"},{"internalType":"uint256","name":"term","type":"uint256"}],"name":"addLicense","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"allocations","outputs":[{"internalType":"uint256","name":"remaining","type":"uint256"},{"internalType":"bool","name":"activated","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"totalAmount","type":"uint256"},{"internalType":"address[]","name":"NFTs","type":"address[]"},{"internalType":"uint256[]","name":"indicies","type":"uint256[]"},{"internalType":"bool","name":"_venture","type":"bool"}],"name":"batchPurchase","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"beginning","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"NFT","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"},{"internalType":"bool","name":"venture","type":"bool"}],"name":"buy","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"claim","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"claimed","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"counterAsset","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"defaultPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"defaultTerm","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"end","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"addedValue","type":"uint256"},{"internalType":"uint256","name":"oldValue","type":"uint256"},{"internalType":"uint256","name":"weightedNew","type":"uint256"},{"internalType":"uint256","name":"weightedOld","type":"uint256"}],"name":"findWeightedAverage","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"totalAmount","type":"uint256"},{"internalType":"address[]","name":"NFTs","type":"address[]"},{"internalType":"uint256[]","name":"indicies","type":"uint256[]"},{"internalType":"bool","name":"venture","type":"bool"}],"name":"getBatchPricing","outputs":[{"components":[{"internalType":"uint256","name":"nftPerShare","type":"uint256"},{"internalType":"uint256","name":"nftTotalCost","type":"uint256"},{"internalType":"uint256","name":"nftTotalShares","type":"uint256"},{"internalType":"uint256","name":"perShare","type":"uint256"},{"internalType":"uint256","name":"totalAvailable","type":"uint256"},{"internalType":"uint256","name":"totalCost","type":"uint256"}],"internalType":"struct ElasticLGE.BatchPricingData","name":"data","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"totalAmount","type":"uint256"},{"internalType":"address[]","name":"NFTs","type":"address[]"},{"internalType":"uint256[]","name":"indicies","type":"uint256[]"},{"internalType":"bool","name":"venture","type":"bool"}],"name":"getBatchTerms","outputs":[{"internalType":"uint256","name":"nftTerm","type":"uint256"},{"internalType":"uint256","name":"term","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"NFT","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"getPricingData","outputs":[{"internalType":"uint256","name":"available","type":"uint256"},{"internalType":"uint256","name":"perShare","type":"uint256"},{"internalType":"uint256","name":"totalCost","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"licenses","outputs":[{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"uint256","name":"limit","type":"uint256"},{"internalType":"uint256","name":"term","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"multisig","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"oath","outputs":[{"internalType":"contract IOath","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"raised","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"shareSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"terms","outputs":[{"internalType":"uint256","name":"shares","type":"uint256"},{"internalType":"uint256","name":"term","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalOath","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOath","type":"address"}],"name":"upgradeOath","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"venturePrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ventureTerm","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]
    
    return contract_abi

# # gets our web3 contract object
def get_contract_object(contract_address, contract_abi, web3):
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    return contract

# # calls the terms function on our smart contract for a given wallet_address
def find_user_terms(contract, wallet_address):
    
    terms = contract.functions.terms(wallet_address).call()

    return terms

def get_user_shares(terms):
    user_shares = terms[0]

    return user_shares

def get_user_uint_term(terms):
    uint_terms = terms[1]

    return uint_terms

#makes a dataframe and stores it in a csv file
def make_user_terms_csv(df):
    old_df = pd.read_csv('user_terms.csv')
    old_df = old_df.drop_duplicates(subset=['buyer_address','buyer_shares','buyer_uint_term'], keep='last')

    combined_df_list = [df, old_df]
    combined_df = pd.concat(combined_df_list)
    combined_df = combined_df.drop_duplicates(subset=['buyer_address','buyer_shares','buyer_uint_term'], keep='last')

    if len(combined_df) >= len(old_df):
        combined_df.to_csv('user_terms.csv', index=False)
        # print('Terms CSV Updated')
    return

# # finds a users terms for a single wallet_address
def find_single_users_terms(wallet_address, contract):

    terms = find_user_terms(contract, wallet_address)

    user_shares = get_user_shares(terms)

    user_uint_term = get_user_uint_term(terms)

    df = pd.DataFrame()

    df['buyer_address'] = [wallet_address]
    df['buyer_shares'] = [user_shares]
    df['buyer_uint_term'] = [user_uint_term]

    print(df)

    return df

# # finds the terms for every user
def find_all_user_terms():

    web3 = get_web_3()

    df = get_oath_lge_buyers_df('oath_ftm_lge_buyers.csv')

    contract_abi = get_oath_lge_abi()

    lge_contract = get_contract_object('0x96662f375a9734654cB57BbFeb31Db9dD7784A7F', contract_abi, web3)

    wallet_address_list = df['buyer_address'].to_list()

    call_wait_time = 1

    wallets_checked = 0
    
    for wallet_address in wallet_address_list:
        exists = False

        try:
            df = find_single_users_terms(wallet_address, lge_contract)
            exists = True
        except:
            pass

        if exists == True:
            make_user_terms_csv(df)

        wallets_checked += 1
        print('Wallets Checked: ', wallets_checked, ' / ', len(wallet_address_list))

        time.sleep(call_wait_time)

        

    # print('Wallet Address: ', wallet_address_list[0])
    # print('Terms: ', terms, ' User Shares: ', user_shares, ' User UINT Term:', user_uint_term)

    return

find_all_user_terms()

df = pd.read_csv('user_terms.csv')

total_shares = df['buyer_shares'].sum()

print(total_shares)