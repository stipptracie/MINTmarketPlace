
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


#################################################################################
#------------------------------ Streamlit app ----------------------------------#
#################################################################################

# Title and info
st.sidebar.title("Mint Market Place")
st.sidebar.write("A place to create an NFT of any file and earn rewards in MINT coin")
st.sidebar.write("You will receive 500 MINT coins for registering your art")
st.sidebar.write("You will also receive a File Token that the NFT for your art")

# account that will be associated with file upload and reward
accounts = w3.eth.accounts

# select account
address = st.sidebar.selectbox("Select Account Associated with File", options=accounts)

st.sidebar.markdown("---")


# choose the file name 
file_name = st.sidebar.text_input("Enter the File Name: ")

# choose creator name
creator_name = st.sidebar.text_input("Enter A Creator Name: ")

# file uploader that allows many different kinds of files
file = st.sidebar.file_uploader("Choose File to Mint", type=[
    "jpeg", "jpg", "png", "pdf", "gif", "txt", "docx", "ppt", "csv", "mp3", "mp4", "wav", "xlsx"
    ])

# Make the button that does it all
if st.sidebar.button("Mint NFT, Receive IPFS file and Receive a Reward"):
    
    # Pin artwork to pinata ipfs file
    file_ipfs_hash = pin_file(file_name=file_name,
                              creator_name=creator_name,
                              desired_file=file, 
                              associated_account=address)
    
    file_uri = f"ipfs://{file_ipfs_hash}"
    print(address, creator_name, file_name, file_uri)
    print(file_ipfs_hash)
    
    
    
    
    # Generate File Token for user address for uploading file
    file_contract = load_file_contract()
    tx_hash_file = file_contract.functions.registerFile(
        address,
        file_uri
    ).transact({'from': address, 'gas': 1000000})
    # receipt for unique file token
    file_token_receipt = w3.eth.waitForTransactionReceipt(tx_hash_file)
    st.sidebar.write("File Minted:")
    tokenID = file_contract.functions.totalSupply().call()
    st.sidebar.write(f"Your NFT is File Token #{tokenID}")
    st.sidebar.write("You can view the pinned metadata file with the following IPFS Gateway Link")
    st.sidebar.markdown(f"[File IPFS Gateway Link](https://ipfs.io/ipfs/{file_ipfs_hash})")
    st.sidebar.markdown(f"Metadata URI: {file_uri}")
    st.sidebar.write(dict(file_token_receipt))
       
    
    # # Mint 500 new MNTs for user address
    # mint_contract = load_mint_contract()
    # #renounce minter
    # mint_contract.functions.renounceMinter().call()
    # print("################# Minter renounced Successfully ###############")
    # # add current address as minter
    # mint_contract.functions.addMinter(address).transact({'from': address, 'gas': 1000000})
    # print("################# New Minter added Successfully ###############")
    # # mint 500 tokens to address
    # mint_hash_file = mint_contract.functions.mint(address, 500).transact({'from': address, 'gas': 1000000})
    
    # mint_token_receipt = w3.eth.waitForTransactionReceipt(mint_hash_file)
    # st.sidebar.write("MINT coins minted:")
    # st.sidebar.write(dict(mint_token_receipt))
    # mint_balance = mint_contract.MintToken.balanceOf(address).call()
    # st.write(f"You now have {mint_balance} MINT coins at address {address}")
    
    
    
    # Print Confirmations
    # st.write("File Minted")
    # st.write(f"You received 1 unique FLT and 500 MNT tokens")
    # st.write(f"Your current balance of MNT is ___ ")
    st.sidebar.balloons() 

#@TODO
# PIN METADATA
# LINK MINT COIN CROWDSALE WITH FILETOKEN






