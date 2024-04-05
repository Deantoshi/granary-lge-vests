import pandas as pd


def make_user_df(base_string, number_of_files):
    i = 1

    df_list = []

    while i <= number_of_files:
        csv_name = base_string + str(i) + '.csv'
        df = pd.read_csv(csv_name)
        df_list.append(df)

        print(csv_name)
        i += 1

    df = pd.concat(df_list)

    wallet_df = pd.DataFrame()
    wallet_df['wallet_address'] = df['From']

    wallet_df = wallet_df.drop_duplicates()

    return wallet_df

def make_csv(new_df, csv_name, chain_name):
    lge_df = pd.read_csv(csv_name)

    new_df['chain'] = chain_name

    df_list = [new_df, lge_df]

    combined_df = pd.concat(df_list)

    print(combined_df)

    combined_df = combined_df.drop_duplicates(subset=['wallet_address', 'chain'])

    if len(combined_df) > len(lge_df):
        combined_df.to_csv('grain_lge_wallets.csv', index=False)
        print('GRAIN LGE CSV Updated')
    return

base_string = 'polygon_lge_'

lge_csv_name = 'grain_lge_wallets.csv'

wallet_df = make_user_df(base_string, 3)

make_csv(wallet_df, lge_csv_name, 'MATIC')

# df = pd.read_csv('grain_remaining_vests.csv')

# df = df.loc[df['chain'] == 'FTM']

# print(df['remaining_vest'].sum())