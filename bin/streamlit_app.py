import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

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
file_contract = load_contract("nftRegistry")

# Set web store owner address to the smart contracts
store_address = os.getenv("STORE_OWNER_WALLET_ADDRESS")

########## NFT Set Up ##########
# Set NFT owner address
seller_address = st.text_input("Put seller's wallet address")
# Accept a file
tokenid = int(st.number_input("Enter tokenid", 0, 50))

#######################
## Save file to IPFS ##
# file = st.file_uploader("Upload Artwork", type=["jpg", "jpeg", "png"])
tokenURI = "Unique IPFS Addres (URL/URI) will be set"
#######################


########## NFT Transfer Ownership ##########
# Set purchaser address
purchaser_address = st.text_input("Enter Purchaser's address")
# Set purchasing price
offer_amount = int(st.number_input("How much would you pay?"))


# FOR DEVELOPING PURPOSE ONLY #
@st.cache(allow_output_mutation=True)
def give_coin_for_developing():
    # Mint coin to store
    coin_contract.functions.mint(store_address, 1000000000).transact({"from": store_address, "gas": 100000})
    # Store -> NFT purchaser
    coin_contract.functions.transfer(purchaser_address, 500000000).transact({"from": store_address, "gas": 100000})
    # Store -> NFT minter
    coin_contract.functions.transfer(seller_address, 500000000).transact({"from": store_address, "gas": 100000})
give_coin_for_developing()


# Transfer NFT and coin
if st.button ("Transfer"):
    ########## Coin Transfer ##########
    # Transfer coin
    coin_contract.functions.approve(seller_address, offer_amount).transact({"from": purchaser_address, "gas": 100000})
    coin_contract.functions.transferFrom(purchaser_address, seller_address, offer_amount).transact({"from":seller_address, "gas":100000})
    #coin_contract.functions.decreaseAllowance(seller_address, offer_amount).transact({"from": purchaser_address, "gas": 100000})

    ########## Coin Offering ##########
    # Mint coin to store
    coin_contract.functions.mint(store_address, 20000).transact({"from": store_address, "gas": 100000})
    # Store -> NFT purchaser
    coin_contract.functions.transfer(purchaser_address, 10000).transact({"from": store_address, "gas": 100000})
    # Store -> NFT minter
    coin_contract.functions.transfer(seller_address, 10000).transact({"from": store_address, "gas": 100000})

    ########## Show Coin Balance ##########
    st.markdown("## Seller Balance")
    st.write(coin_contract.functions.balanceOf(seller_address).call())
    st.markdown("## Purchaser Balance")
    st.write(coin_contract.functions.balanceOf(purchaser_address).call())


    ########## NFT Transfer ##########
    file_contract.functions.transferFrom(seller_address, purchaser_address, tokenid).transact({"from": seller_address, "gas": 100000})
    # Display owner
    st.markdown(f"## Current Owner of the NFT token id {tokenid}")
    st.write(file_contract.functions.ownerOf(tokenid).call())


    st.markdown("# Thank you for participating")
