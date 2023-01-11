
# Main file for pinning files to ipfs system and generating metadata
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
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


    with open(Path('./compiled_contracts/in_app_coin_abi.json')) as f:

        
    # 1. Load MintToken contract
    mint_contract = w3.eth.contract(
        address=mint_contract_address,
        abi=mint_abi
    )
    return mint_contract

# 2. Load FileToken contract
@st.cache(allow_output_mutation=True)
def load_file_contract():
    
    file_contract_address = os.getenv("FILE_REGISTRY_ADDRESS")


    with open(Path('./compiled_contracts/file_registry_abi.json')) as f:

        file_token_abi = json.load(f)

    file_token_contract = w3.eth.contract(
        address=file_contract_address,
        abi=file_token_abi
    )
    return file_token_contract

#################################################################################
#------------------------------ Coin Functions ---------------------------------#
#################################################################################

### Mint Coins for Initial Supply ###
# Set store owner
store_owner_address = os.getenv("STORE_OWNER_ADDRESS")
# Load MINT token contract
mint_contract = load_mint_contract()
# Define function for minting intial coin to store owner 
initial_supply_mint = w3.toWei(1000000000, "ether")

@st.cache(allow_output_mutation=True)
def mint_coin_for_owner():
    mint_contract.functions.mint(store_owner_address, initial_supply_mint).transact({
        "from": store_owner_address, "gas": 100000})

    reward_message = "1000000000 MINT coins have been put into circulation"
    print(reward_message)
    
# call function to mint intial supply
# add sessino state to this function
mint_coin_for_owner()




# define transfer function for 
@st.cache(allow_output_mutation=True)
def reward_coin(store_owner, recipient_address, amount):
    mint_contract.functions.transfer(
        recipient=recipient_address, amount=amount
        ).transact({
        "from": store_owner, "gas": 100000
        })

    # set approval for rewardee to spend rewarded coin
    mint_contract.functions.approve(recipient_address, amount).transact({
        "from": store_owner, "gas": 100000
    })


@st.cache(allow_output_mutation=True)
def get_balance(address):
    mint_contract.functions.balanceOf(address)


#################################################################################
#------------------------------ Create NFT Registry ----------------------------#
#################################################################################

# Create pandas dataframe of registry info
# Try reading the data

columns=["TokenID", "FileName", "IPFS"]
try:    
    registry_df = pd.read_csv(Path('./nft_registry.csv'))
    registry_df = registry_df.astype({"TokenID": "int"})
    registry_df = registry_df.astype({"FileName": "string"})
    registry_df = registry_df.astype({"IPFS": "string"})
except:
    
    registry_df = pd.DataFrame(columns=columns)
    # change datatypes to int, string, string
    registry_df = registry_df.astype({"TokenID": "int"})
    registry_df = registry_df.astype({"FileName": "string"})
    registry_df = registry_df.astype({"IPFS": "string"})


#################################################################################
#------------------------------ Streamlit app ----------------------------------#
#################################################################################


#----------------------------- Sidebar Registry --------------------------------#

# Title and info
st.sidebar.title("Mint Market Place")
st.sidebar.write("A place to create an NFT of any file and earn rewards in MINT coin")
st.sidebar.write("You will receive 500 MINT coins for registering your art")
st.sidebar.write("You will also receive a File Token that is the NFT ID for your art")

# Initialize file registry contract
file_contract = load_file_contract()

# account that will be associated with file upload and reward
accounts = w3.eth.accounts

# select account
address = st.sidebar.selectbox(

    "Select Account Associated with File", options=accounts, key="creator_account")


st.sidebar.markdown("---")


# choose the file name 

file_name = st.sidebar.text_input("Enter the File Name: ", key="file_name")

# choose creator name
creator_name = st.sidebar.text_input("Enter A Creator Name: ", key="creator_name")


# file uploader that allows many different kinds of files
file = st.sidebar.file_uploader("Choose File to Mint", type=[
    "jpeg", "jpg", "png", "pdf", "gif", 
    "txt", "docx", "ppt", "csv", "mp3", "mp4", "wav", "xlsx"

    ], key="nft_file")




# Make the button that does it all

if st.sidebar.button("Mint NFT, Receive IPFS file and Receive a Reward", key="nft_button"):

    
    # Pin artwork to pinata ipfs file
    file_ipfs_hash = pin_file(file_name=file_name,
                              creator_name=creator_name,
                              desired_file=file, 
                              associated_account=address)
    
    file_uri = f"ipfs://{file_ipfs_hash}"
    print(address, creator_name, file_name, file_uri)
    print(file_ipfs_hash)
    
    # Generate File Token for user address for uploading file
    tx_hash_file = file_contract.functions.registerFile(
        address,
        file_uri
    ).transact({'from': address, 'gas': 1000000})
    # receipt for unique file token
    file_token_receipt = w3.eth.waitForTransactionReceipt(tx_hash_file)
    st.sidebar.write("File Minted:")
    
    tokenID = file_contract.functions.totalSupply().call()

    tokenID = (tokenID - 1)

    
    st.sidebar.write(f"Your NFT is File Token #{tokenID}")
    st.sidebar.write("You can view the pinned metadata file with the following IPFS Gateway Link")
    st.sidebar.markdown(f"[File IPFS Gateway Link](https://ipfs.io/ipfs/{file_ipfs_hash})")
    st.sidebar.write(dict(file_token_receipt))
    # Transfer 500 coins from store owner to person who registers
    # convert 500 wei to eth
    reward = w3.toWei(500, "ether")
    reward_coin(
        store_owner=store_owner_address,
        recipient_address=address, 
        amount=reward)
    print("Coins rewarded")
    # Show balance of MINT coins at bottom of sidebar
    balance_wei = mint_contract.functions.balanceOf(address).call()
    balance_ether = w3.fromWei(balance_wei, "ether")
    st.sidebar.write(f"You have a balance of {balance_ether:.2f} MINT coins!")
    st.sidebar.balloons() 
    
    
    ### Update NFT dictionary

    nft_data = {"TokenID": [tokenID],
               "FileName": [file_name],
                "IPFS": [file_uri]}
    nft_df = pd.DataFrame(nft_data, columns=columns)
    nft_df = nft_df.astype({"TokenID": "int"})
    nft_df = nft_df.astype({"FileName": "string"})
    nft_df = nft_df.astype({"IPFS": "string"})
    
    # turn nft_data to a dataframe
    print("registry dataframe")
    print(registry_df)
    registry_df = pd.concat([registry_df, nft_df])
    registry_df.to_csv("nft_registry.csv", index=False)


           
    

#@TODO
# Display for what has been registered so far


#----------------------------- NFT Transfer ------------------------------------#

st.title("Buy a Previously Minted NFT")

buy_col, display_col = st.columns(2)


with buy_col:
        buyer = st.text_input("Enter the Buyer's Address")
        buyer = buyer.strip('"')
#         #@TODO
        amount_of_sale = st.number_input("Enter amount to buy in eth", key="amount_of_sale")
        amount_of_sale = int(amount_of_sale)
        # Select NFT to buy
        options = []
        try:
            for row in registry_df.iterrows():
                options.append(row[1][0])
            option = st.selectbox(label="Pick the NFT you would like to buy",options=options)  
        except:
            pass
        # Set seller as owner of NFT
        try:
            nft_owner = file_contract.functions.ownerOf(option).call()
            nft_owner = nft_owner.strip('"')
            st.write(f"The owner of nft {option} is {nft_owner}")
        except:
            pass
            
        # transfer funds from buyer to seller
        # if transfer successful
        if st.button("Buy NFT Now", key="buy_button"):
            
            mint_contract.functions.approve(
                    buyer, amount_of_sale).transact({
                        "from": buyer, "gas": 1000000
                })
            # Approve transfer ability for owner of NFT
            mint_contract.functions.transferFrom(
                    buyer, nft_owner.strip("'"), int(amount_of_sale)).transact({
                        "from": buyer, "gas": 1000000
                })
            
                # decrease spending allowance for buyer by amount spent
            mint_contract.functions.decreaseAllowance(
                buyer, amount_of_sale).transact({
                    "from": buyer, "gas": 1000000
            })
            st.write("Successful Sale")
            
            # Approve movement of NFT
            file_contract.functions.approve(buyer.strip('"'), int(option)).transact({
                "from": nft_owner, "gas": 1000000
            })
            
            # Next complete transfer of nft to new owner
            file_contract.functions.transferFrom(nft_owner, buyer.strip('"'), int(option)).transact({
                "from": buyer, "gas": 1000000
            })
            st.write("successful transfer of NFT")
            
            new_owner = file_contract.functions.ownerOf(option).call()
            print(f"{new_owner} is now owner of File: {option}")
            st.write(f"{new_owner} is now owner of File: {option}")
        
            mint_contract.functions.transferFrom(
            nft_owner, buyer,  amount_of_sale).transact({
                "from": nft_owner, "gas": 1000000
        })
            print("Sale reverted and NFT transfer did not occur")
      

    
with display_col:
    st.write("NFT Registry")
    # nft_df = pd.DataFrame(registry_info)
    try:
        st.dataframe(registry_df)
    except:
        pass




