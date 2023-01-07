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
file_contract = load_contract("FileRegistry")
auction_contract = load_contract("AuctionContract")

# Set web store owner address to the smart contracts
store_address = os.getenv("STORE_OWNER_WALLET_ADDRESS")





########## NFT Set Up ##########
# Set NFT owner address
seller_address = st.text_input("Put seller's wallet address")
# Accept a file
name_of_file = st.text_input("Enter the name of the file")
name_of_owner = st.text_input("Enter the name of the owner")
file = st.file_uploader("Upload Artwork", type=["jpg", "jpeg", "png"])

#######################
## Save file to IPFS ##
tokenURI = "Unique IPFS Addres (URL/URI) will be set"
#######################

# Assign NFT to a file
tokenid = file_contract.functions.registerFile(seller_address, name_of_file, name_of_owner, tokenURI).transact({"from": seller_address, "gas": 6721970})
# Display token ID
st.write(tokenid)

# # Set offer amount
offer_amount = int(st.number_input("How much would you pay?"))
# Set purchaser equal to the highest bidder
purchaser_address = st.text_input("Enter Purchaser's address")
# Transfer NFT
file_contract.functions.transferFrom(seller_address, purchaser_address, tokenid).transact({"from": seller_address, "gas": 100000})
# Transfer Coin
coin_contract.function.transfer(seller_address, offer_amount).transact({"from":purchaser_address, "gas": 100000})


########## Coin Offering ##########
# Store -> NFT purchaser
coin_contract.function.transfer(purchaser_address, offer_amount).transact({"from": store_address, "gas": 100000})
# Store -> NFT minter
coin_contract.function.transfer(seller_address, offer_amount).transact({"from": store_address, "gas": 100000})


########## Display NFT Status ##########

# Owner (Should match the purchaser's address)
file_contract.functions.ownerOf(tokenid).call()