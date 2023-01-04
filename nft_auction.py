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
file = 'st.file_uploader("Upload Artwork", type=["jpg", "jpeg", "png"])'

#######################
## Save file to IPFS ##
tokenURI = "Unique IPFS Addres (URL/URI) will be set"
#######################

# Assign NFT to a file
tokenid = file_contract.functions.registerFile(seller_address, name_of_file, name_of_owner, tokenURI).transact({"from": seller_address, "gas": 6721970})





########## Auction ##########
st.write(auction_contract.functions.store().transact({"from": seller_address, "gas": 6721970}))

### Start ###
# Set Starting Price
starting_price = int(st.number_input("Starting Price"))
# Start Auction
if st.button("Start Auction"):
    auction_contract.functions.start(starting_price).transact({"from": seller_address, "gas": 6721970})

### Bid ###
# Set Auction Bidder address
bidder_address = st.text_input("Put purchaser wallet address")
# Set Bidding Amount
amount = int(st.number_input("Bid Amount"))
# Bid
if st.button("Bid"):
    auction_contract.functions.bid(amount).transact({"from": bidder_address, "gas": 100000})

if st.button("What time is this auction end at?"):
    st.write(auction_contract.functions.endAt().transact({"from": seller_address, "gas": 100000}))

### End ###
if st.button("end"):
    auction_contract.functions.end().transact({"from": seller_address, "gas": 100000})


    ########## NFT and Coin Transfer ##########
    
    # # Set offer amount
    offer_amount = auction_contract.functions.highestBid().transact({"from": seller_address, "gas": 100000})
    st.write(offer_amount)
    # Set purchaser equal to the highest bidder
    purchaser_address = auction_contract.functions.highestBidder().transact({"from": seller_address, "gas": 100000})
    st.write(purchaser_address)
    # Transfer NFT
    file_contract.functions.transferFrom(seller_address, purchaser_address, tokenid).transact({"from": seller_address, "gas": 100000})
    # Transfer Coin
    coin_contract.function.transfer(seller_address, offer_amount).transact({"from":purchaser_address, "gas": 100000})


    ########## Coin Offering ##########
    # Store -> NFT purchaser
    coin_contract.function.transfer(purchaser_address, offer_amount).transact({"from": store_address, "gas": 100000})
    # Store -> NFT minter
    coin_contract.function.transfer(seller_address, offer_amount).transact({"from": store_address, "gas": 100000})


    ########## Display Winner and NFT Details ##########
    # Winner
    auction_contract.functions.highestBidder().call()
    # Price
    auction_contract.functions.highestBid().call()
    # Owner (Should match the winner's address)
    file_contract.functions.ownerOf(tokenid).call()