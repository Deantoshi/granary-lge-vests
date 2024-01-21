import pandas as pd
from google.cloud import storage
import google.cloud.storage
import json
import os
import sys

PATH = os.path.join(os.getcwd(), 'yuzu-api-01-50ed5aff527c.json')
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
def read_from_cloud_storage():
    storage_client = storage.Client(PATH)
    print(storage_client)

    bucket = storage_client.get_bucket('yuzu_transactions')

    print(bucket)

    filename = [filename.name for filename in list(bucket.list_blobs(prefix='')) ]
    print(filename)

    # download the csv file
    blop = bucket.blob(blob_name = 'user_transactions.csv').download_as_string()

    with open ('user_transactions.csv', "wb") as f:
        f.write(blop)
    
    df = pd.read_csv('user_transactions.csv')

    df = df[['wallet_address', 'token_name', 'number_of_tokens', 'reserve_address', 'tx_hash', 'block_number', 'last_block_number', 'q_made_transaction', '10_zen_deposited', '001_wbtc_deposited', '25_usdc_borrowed', '02_weth_borrowed']]

    return df

# takes in our filename and bucket and uploads our csv to our bucket
def write_to_cloud_storage():
    filename = 'user_transactions.csv'
    uploadfile = os.path.join(os.getcwd(), filename)

    storage_client = storage.Client(PATH)

    bucket = storage_client.get_bucket('yuzu_transactions')
    blob = bucket.blob(filename)
    blob.upload_from_filename(uploadfile)

    return

# read_from_cloud_storage()

write_to_cloud_storage()