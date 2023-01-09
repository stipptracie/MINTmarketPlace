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
def load_coin_contract():

    mint_contract_address = os.getenv("InAppCoin_TOKEN_ADDRESS")

    with open(Path('/contracts/compiled/InAppCoin_abi.json')) as f:
        coin_abi = json.load(f)
        
    # 1. Load MintToken contract
    coin_contract = w3.eth.contract(
        address=mint_contract_address,
        abi=coin_abi
    )
    return coin_contract

# 2. Load FileToken contract
@st.cache(allow_output_mutation=True)
def load_file_contract():
    
    file_contract_address = os.getenv("FILE_TOKEN_ADDRESS")

    with open(Path('/contracts/compiled/file_token_abi.json')) as f:
        file_token_abi = json.load(f)

    file_token_contract = w3.eth.contract(
        address=file_contract_address,
        abi=file_token_abi
    )

    return file_token_contract

#################################################################################
#------------------------------ Coin transfers ---------------------------------#
#################################################################################
# Set web store owner address to the smart contracts
store_address = os.getenv("STORE_OWNER_WALLET_ADDRESS")

### Mint Some Coin First For Developing ###
@st.cache(allow_output_mutation=True)
def mint_coin_for_developing():
    coin_contract = load_coin_contract()
    coin_contract.functions.mint(store_address, 1000000000).transact({"from": store_address, "gas": 100000})
mint_coin_for_developing()

@st.cache(allow_output_mutation=True)
def transfer_coin_from_store_to_address(address, amount):
    coin_contract = load_coin_contract()
    coin_contract.functions.transfer(address, amount).transact({"from": store_address, "gas": 100000})

#################################################################################
#------------------------------ Streamlit app ----------------------------------#
#################################################################################


### Main Page ###
st.title("MINT Marketplace")
st.write("A place to create an NFT of any file and earn rewards in MINT coin")
st.write("You can sell your registered")
st.write("You will receive 500 MINT coins for registering your art")
st.write("You will also receive a File Token that the NFT for your art")


### Sidebar ###

# Title and info
st.sidebar.title("Register Your NFT as a File Token")


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
    coin_contract = load_coin_contract()
    transfer_coin_from_store_to_address(address, 500)
    st.write("Coins Created:")
    coin_balance = st.write(coin_contract.functions.balanceOf(address).call())
    st.write(f"You now have {coin_balance} MINT coins at address {address}")
    
    st.sidebar.balloons() 

########## Transfer NFT and reward coin ##########
# Set purchasing price and address
offer_amount = int(st.sidebar.number_input("How much would you pay?"))
purchaser_address = st.sidebar.selectbox("Select Buyer's Account", options=accounts)

if st.sidebar.button ("Transfer NFT Ownership"):
    #################### FOR DEVELOPING PURPOSE ONLY ####################
    #### Give out coins to purchaser to simulate buy-sell activities ####
    transfer_coin_from_store_to_address(purchaser_address, 50000)
    #####################################################################

    ########## Coin Transfer ##########
    # Transfer coin
    coin_contract.functions.transfer(address, offer_amount).transact({"from":purchaser_address, "gas": 100000})

    ########## Coin Offering ##########
    # Store -> NFT purchaser
    coin_contract.functions.transfer(purchaser_address, 500).transact({"from": store_address, "gas": 100000})
    # Store -> NFT minter
    coin_contract.functions.transfer(address, 500).transact({"from": store_address, "gas": 100000})

    ########## Show Coin Balance ##########
    st.sidebar.markdown("## Seller Balance")
    st.sidebar.write(coin_contract.functions.balanceOf(address).call())
    st.sidebar.markdown("## Purchaser Balance")
    st.sidebar.write(coin_contract.functions.balanceOf(purchaser_address).call())


    ########## NFT Transfer ##########
    nft_id = int(file_contract.functions.totalSupply().call())
    st.sidebar.write(nft_id)
    file_contract.functions.transferFrom(address, purchaser_address, nft_id).transact({"from": store_address, "gas": 5555555})
    # Display owner
    st.sidebar.markdown(f"## Current Owner of the NFT token id {nft_id}")
    st.sidebar.write(file_contract.functions.ownerOf(nft_id).call())


    st.sidebar.markdown("# Thank you for participating")