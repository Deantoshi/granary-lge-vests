import pandas as pd
from google.cloud import storage
import google.cloud.storage
import json
import os
import sys
import io
from io import BytesIO


PATH = os.path.join(os.getcwd(), 'yuzu-api-01-dae6611de7aa.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = PATH

# # writes to our cloud storage object
# def write_to_cloud_storage():
#     # loads the dataframe
#     df = pd.read_csv('user_transactions.csv')

#     # load our data into our google cloud service
#     client = storage.Client()
#     export_bucket = client.get_bucket('yuzu_transactions')

#     # bucket.blob(file_name).upload()
#     export_bucket.blob('user_transactions.csv').upload_from_string(df.to_csv(), 'text/csv')

#     return

# reads as the name implies
def read_from_cloud_storage(input_filename):
    storage_client = storage.Client(PATH)
    # print(storage_client)

    bucket = storage_client.get_bucket('yuzu_transactions')

    # print(bucket)

    filename = [filename.name for filename in list(bucket.list_blobs(prefix='')) ]
    # print(filename)

    # download the csv file
    # blop = bucket.blob(blob_name = 'user_transactions.csv').download_as_string()

    blop = bucket.blob(blob_name = input_filename).download_as_string()

    with open (input_filename, "wb") as f:
        f.write(blop)
    
    df = pd.read_csv(input_filename)

    if input_filename == 'user_transactions.csv':
        df = df[['wallet_address', 'token_name', 'number_of_tokens', 'reserve_address', 'tx_hash', 'block_number', 'last_block_number', 'q_made_transaction', '10_zen_deposited', '001_wbtc_deposited', '25_usdc_borrowed', '02_weth_borrowed']]

    elif input_filename == 'cooldown.csv':
        df = df[['next_update_timestamp']]

    return df


def read_from_cloud_storage_2():
    storage_client = storage.Client(PATH)
    bucket = storage_client.get_bucket('yuzu_transactions')

    df = pd.read_csv(
    io.BytesIO(
                 bucket.blob(blob_name = 'user_transactions.csv').download_as_string() 
              ) ,
                 encoding='UTF-8',
                 sep=',')
    return df

# takes in our filename and bucket and uploads our csv to our bucket
def write_to_cloud_storage(filename):
    # filename = 'user_transactions.csv'
    uploadfile = os.path.join(os.getcwd(), filename)

    storage_client = storage.Client(PATH)

    bucket = storage_client.get_bucket('yuzu_transactions')
    blob = bucket.blob(filename)
    blob.upload_from_filename(uploadfile)

    return

def df_write_to_cloud_storage(df, filename):

    storage_client = storage.Client(PATH)
    bucket = storage_client.get_bucket('yuzu_transactions')

    csv_string = df.to_csv(index=False)  # Omit index for cleaner output
    # print(csv_string)
    blob = bucket.blob(filename)
    blob.upload_from_string(csv_string)
    # print('')

    return

# read_from_cloud_storage()

# filename = 'cooldown.csv'
# filename = 'user_transactions.csv'
# write_to_cloud_storage(filename)

# print(read_from_cloud_storage(filename))

# df = pd.read_csv('cooldown.csv')
# df_write_to_cloud_storage(df, 'cooldown.csv')

df = read_from_cloud_storage_2()
print(df)