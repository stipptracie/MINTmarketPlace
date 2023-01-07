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

#################################################################################
#-------------------------------- IFPS Helper ----------------------------------#
#################################################################################

# Define function for generating pinata pin
def pin_file(file_name, associated_account, creator_name, desired_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(desired_file.getvalue())

    # Build a token metadata file for the artwork
    token_json = {
        "name": file_name,
        "creator": creator_name,
        "file": ipfs_file_hash,
        "associated_account": associated_account
    }
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash

#################################################################################
#------------------------------ Smart Contracts --------------------------------#
#################################################################################

# Load MintToken and FileToken abis

@st.cache(allow_output_mutation=True)
def load_mint_contract():

    mint_contract_address = os.getenv("MINT_TOKEN_ADDRESS")

    with open(Path('./compiled_contracts/mint_abi.json')) as f:
        mint_abi = json.load(f)
        
    # 1. Load MintToken contract
    mint_contract = w3.eth.contract(
        address=mint_contract_address,
        abi=mint_abi
    )
    return mint_contract

# 2. Load FileToken contract
@st.cache(allow_output_mutation=True)
def load_file_contract():
    
    file_contract_address = os.getenv("FILE_TOKEN_ADDRESS")

    with open(Path('./compiled_contracts/file_token_abi.json')) as f:
        file_token_abi = json.load(f)

    file_token_contract = w3.eth.contract(
        address=file_contract_address,
        abi=file_token_abi
    )
    return file_token_contract