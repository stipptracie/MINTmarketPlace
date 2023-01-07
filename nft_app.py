# Imports
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
# personalized functions for api usage
from ipfs.pinata_helper import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json


load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

#################################################################################
#--------------------------- Load Smart Contracts-------------------------------#
#################################################################################

# Define a function to load contracts
@st.cache(allow_output_mutation=True)
def load_contract(contract_name):

    # Load ABI
    with open(Path(f"contracts/compiled/{contract_name}_abi.json")) as f:
        abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv(f"{contract_name}_SMART_CONTRACT_ADDRESS")

    # Get the contract using web3
    contract = w3.eth.contract(address=contract_address, abi=abi)

    return contract

# Load contracts
coin_contract = load_contract("InAppCoin")
file_contract = load_contract("file_token")

# Set web store owner address to the smart contracts
store_address = os.getenv("STORE_OWNER_WALLET_ADDRESS")

#################################################################################
#------------------------------ Coin transfers ---------------------------------#
#################################################################################
### Mint Some Coin First For Developing ###
@st.cache(allow_output_mutation=True)
def mint_coin_for_developint():
    coin_contract.functions.mint(store_address, 1000000000).transact({"from": store_address, "gas": 100000})
mint_coin_for_developint()

@st.cache(allow_output_mutation=True)
def transfer_coin_from_store_to_address(address, amount):
    coin_contract.functions.transfer(address, amount).transact({"from": store_address, "gas": 100000})


#################################################################################
#-------------------------------- IFPS Helper ----------------------------------#
#################################################################################

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
#----------------------- Streamlit app - Main ----------------------------------#
#################################################################################

# Title and info
st.title("Mint Market Place")
st.write("A place to create an NFT of any file and earn rewards in MNT")
st.write("You will receive a commission of MNT tokens for registering your art")
st.write("You will also receive a File Token that is your NFT for your art")
st.write("Choose an account to get started")

# account that will be associated with file upload and reward
accounts = w3.eth.accounts

# select account
seller_address = st.selectbox("Select Account Associated with File", options=accounts)

st.markdown("---")


# choose the file name 
file_name = st.text_input("Enter the File Name: ")

# choose creator name
creator_name = st.text_input("Enter A Creator Name: ")

# file uploader that allows many different kinds of files
file = st.file_uploader("Choose File to Mint", type=[
    "jpeg", "jpg", "png", "pdf", "gif", "txt", "docx", "ppt", "csv", "mp3", "mp4", "wav", "xlsx"
    ])

# Make the button that does it all
if st.button("Mint NFT and Receive a Reward"):
    
    # Pin artwork to pinata ipfs file
    file_ipfs_hash = pin_file(file_name=file_name, desired_file=file, associated_account=seller_address)
    file_uri = f"ipfs://{file_ipfs_hash}"
    print(seller_address, file_name, file_uri)
        
    # Generate FLT for user address for uploading file
    tx_hash_file = file_contract.functions.registerFile(seller_address, file_uri).transact({'from': seller_address, 'gas': 1000000})
    # receipt for unique file token
    file_token_receipt = w3.eth.waitForTransactionReceipt(tx_hash_file)
    st.write("File Minted:")
    st.write(dict(file_token_receipt))
            
    # mint 500 InAppCoin to address as a reward for participating
    mint_hash_file = transfer_coin_from_store_to_address(seller_address, 500)
    ico_receipt = w3.eth.waitForTransactionReceipt(mint_hash_file)
    st.write("Coins Created:")
    st.write(dict(ico_receipt))
    coin_balance = st.write(coin_contract.functions.balanceOf(seller_address).call())
    st.write(f"You now have {coin_balance} MINT coins at address {seller_address}")
    
    # Print Confirmations
    st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
    st.markdown(f"[File IPFS Gateway Link](https://ipfs.io/ipfs/{file_ipfs_hash})")
    st.markdown(f"{file_uri}")
    st.balloons()
   

#################################################################################
#------------------------ Streamlit app - Sidebar ------------------------------#
#################################################################################
########## NFT Transfer Ownership ##########
# Title and descriptions
st.sidebar.title("NFT Transfer")


# Transfer NFT and coin
if st.sidebar.button ("Transfer NFT Ownership"):
    # Set purchaser address
    purchaser_address = st.sidebar.text_input("Enter Purchaser's address")

    #################### FOR DEVELOPING PURPOSE ONLY ####################
    #### Give out coins to purchaser to simulate buy-sell activities ####
    transfer_coin_from_store_to_address(purchaser_address)
    #####################################################################

    # Set purchasing price
    offer_amount = int(st.sidebar.number_input("How much would you pay?"))

    ########## Coin Transfer ##########
    # Transfer coin
    coin_contract.functions.approve(seller_address, offer_amount).transact({"from": purchaser_address, "gas": 100000})
    coin_contract.functions.transferFrom(purchaser_address, seller_address, offer_amount).transact({"from":seller_address, "gas":100000})
    #coin_contract.functions.decreaseAllowance(seller_address, offer_amount).transact({"from": purchaser_address, "gas": 100000})

    ########## Coin Offering ##########
    # Store -> NFT purchaser
    coin_contract.functions.transfer(purchaser_address, 500).transact({"from": store_address, "gas": 100000})
    # Store -> NFT minter
    coin_contract.functions.transfer(seller_address, 500).transact({"from": store_address, "gas": 100000})

    ########## Show Coin Balance ##########
    st.markdown("## Seller Balance")
    st.write(coin_contract.functions.balanceOf(seller_address).call())
    st.markdown("## Purchaser Balance")
    st.write(coin_contract.functions.balanceOf(purchaser_address).call())


    ########## NFT Transfer ##########
    tokenid = file_contract.functions.tokenId().call()
    file_contract.functions.transferFrom(seller_address, purchaser_address, tokenid).transact({"from": seller_address, "gas": 100000})
    # Display owner
    st.markdown(f"## Current Owner of the NFT token id {tokenid}")
    st.write(file_contract.functions.ownerOf(tokenid).call())


    st.markdown("# Thank you for participating")
