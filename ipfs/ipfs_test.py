# import required libraries

import os
import json
import requests
from pathlib import Path
import streamlit as st
import ipfshttpclient
from dotenv import load_dotenv
from web3 import Web3
from pinata import Pinata
# functions for pinata


# load environment variables
load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# Create pinata env variables
api_key = os.getenv("PINATA_API_KEY")
secret_key = os.getenv("PINATA_SECRET_KEY")
access_token = os.getenv("JWT")

# Load pinata client
pinata = Pinata(api_key=api_key, secret_key=secret_key, access_token=access_token)

# # pinata api url
# pinata_url = "https://api.pinata.cloud"


# import requests
# url = "https://api.pinata.cloud/data/testAuthentication"
# payload={} 
# headers = {'Authorization': f'Bearer {access_token}'}
# response = requests.request("GET", url, headers=headers, data=payload)
# print(response.text)

def pin_to_pinata(file_name, identity, file_path):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    payload={'pinataOptions': "{'cidVersion': 1}",
             
             'pinataMetadata': "{'name': f"{file_name}",
             
             'keyvalues': "{'id': f'{identity}'}"
             
             }
             
    files=[
        ('file',(file_name, open(file_path,'rb'), 'application/octet-stream'))
           ]
    headers = {
        'Authorization': f'Bearer {access_token}'
               }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)

# Stramlit app #

# st.markdown("# Pinata IPFS test")

# # Upload Box
# data = st.file_uploader("Upload Artwork Here")

# Create Register Button
# if st.button("Register NFT"):