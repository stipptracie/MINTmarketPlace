# Main file for pinning files to ipfs system and generating metadata
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
# personalized functions for api usage
from pinata_helper import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

# load environment variables
load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB_PROVIDER_URI")))

# Define function for generating pinata pin
def pin_file(file_name, associated_account, desired_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(desired_file.getvalue())

    # Build a token metadata file for the artwork
    token_json = {
        "name": file_name,
        "file": ipfs_file_hash,
        "associated_account": associated_account
    }
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash

#################################################################################
#------------------------------ Streamlit app ----------------------------------#
#################################################################################

st.title("IPFS File Uploader")
st.write("Choose an account to get started")

# account that will be associated with file upload
accounts = w3.eth.accounts
address = st.selectbox("Select Account Associated with File", options=accounts)
st.markdown("---")

# file name 
file_name = st.text_input("Enter the File Name: ")


# file uploader that allows many different kinds of files
file = st.file_uploader("Choose File to Mint", type=[
    "jpeg", "jpg", "png", "pdf", "gif", "txt", "docx", "ppt", "csv", "mp3", "mp4", "wav", "xlsx"
    ])

if st.button("Mint and Receive a Reward"):
    artwork_ipfs_hash = pin_file(file_name=file_name, desired_file=file, associated_account=address, )
    artwork_uri = f"ipfs://{artwork_ipfs_hash}"
    
    
    st.write("File Minted")
    st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
    st.markdown(f"[File IPFS Gateway Link](https://ipfs.io/ipfs/{artwork_ipfs_hash})")
    st.balloons






