# FinTech Capstone: NFT Marketplace

## Table of Contents
* [Description](#description)
* [Goals](#project-goals)
* [Data Collection and Preparation](#data-collection-and-preparation)
* [Development and Technologies](#development-and-technologies)
* [Instructions](#instructions)
* [Video Demo](#video-demo)
* [Outcome And Summary](#outcome-and-summary)
* [Contributors](#contributors)
* [References and Resources](#references-and-resources)



## Description
---
In this project, we aim to create an NFT marketplace decentralized application (dapp) for the auction of digital assets using smart contracts, solidity and streamlit.

## Goals
---

###################![alt=""](.png)</br>####################

In recent years, there has been an ever increasing interest in NFTs - As an example, one NFT which was just an image of a column written in New York Times sold for $560,000 in a matter of days. Observing such keen interest in the demand and sale of NFTs as well as the expanding market for digital assets, we felt it would be a great idea to launch our very own MINT Auction Marketplace. 

MINT's goal is to support local and emerging artists and provide them a fast and efficient FinTech platform to register their work and sell them through an auction-based marketplace allowing them to connect with collectors all over the world through a decentralized network.

Our NFT auction marketplace provides:
1. A platform that connects artists and collectors through blockchain technology with complete transparency. It holds asset/token/deed that is to be auctioned using ERC721 standards.
2. Ability to place bids in auctions, over a decentralized network with following functions and features: </br>
>
        - ability to participate in an English auction whereby bid prices keep increasing over the duration of the auction.
        - ability to monitor the auction process (start bid, bid price, highest bidder etc.)
        - ability to view the frequency of each bidder
        - safe and secure transfer of NFT ownership upon auction completion
        - safe and secure transfer of funds upon auction completion
        - refund of funds to bidders that did not get not lucky
3. Works with digital assests stored over an established and secure file storage system (IPFS - Pinata)
5. MINT does not charge any fees or retain any of the profits from the NFT sales hence providing a free of cost platform for the artists. As opposed to OpenSea, who charge a chunky one-time registration fee to list each NFT as well as recurring fees.

## Development and Technologies
---

Our NFT marketplace is build using the following technologies: 
* Solidity (smart contracts)
* Remix IDE
* Streamlit (frontend)
* MetaMask (wallet)
* Decentralized Blockchain Network (Ganache)
* Pinata
* Python

### Libraries Used
* os
* json
* requests
* eth_account
* eth_typing
* web3
* pathlib
* dotenv
* streamlit
* dataclasses
* typing
* openzeppelin (ERC721, ERC721URIStorage, Ownable, Counters)

##########################![alt=""](.png)</br>##########################
##########################![alt=""](.png)</br>##########################


## Instructions - Environment Preparation
---
### Files:
Download the following files to help you get started:

1. ##########################[AuctionRegistry.sol](./Final/AuctionRegistry.sol)
2. ##########################[Auction.sol](Final/auction.sol)
 

### Add to ___________ MetaMask steps:

1. Open MetaMask and select `Settings`
2. Select `Networks`
3. Select `Add Network`
4. Enter Network Name `_______`
5. Enter New RPC URL `https://`
6. Enter Chain ID `_______`
7. Enter Currency Symbol `_____`
8. Enter Block Explorer URL `https://__________________`

### Obtain RPC Server Address

Ganache - Backup Project Blockchain - Simply copy RPC Server from Ganache UI.

### Load Keys In .env File

1. Load `PINATA_API_KEY` and `PINATA_SECRET_API_KEY` to .env file for IPFS Hashing and Storage
2. Load `WEB3_PROVIDER_URI` with RPC Server address.
3. Load `SMART_CONTRACT_ADDRESS` according to streamlit dapp. NFTRegistry dapp requires the `##########################` contract address when deployed from Remix. Auction dapp requires `##########################` contract address when deployed from Remix.
4. Load wallet's `________` seed phrase.

### Remix Steps:

To run the application, clone the code from this GitHub repository.

1. Compile the `##########################` to ensure it compiles without any errors. 

2. Compile the `##########################` to ensure it is compiled successfully.

3. Prior to deployment, ensure your MetaMask/wallet is connected and the corresponding item (Injected Web3 for Remix IDE) is selected.

4. Deploy the `##########################` and check the deployed contracts to ensure it is there. Copy the address as it would be required for the next step.

5. Add the `##########################` contract address to the Deploy the AuctionRegistry.sol and proceed to deploy the AuctionRegistry.sol

6. In `##########################` deployed contract, use the address of the Auction contract in the SetApprovalForAll input field and a value of true to ensure the NFT that will be registered can participate in the Auction.

7. In `##########################` deployed contract, use the registerNFT fields to provide an address ownner and key NFT details and register it for the Auction.

8. To proceed with the auction process on the registered NFT, please follow the steps demonstrated in the Auction Demo (see Videos Demos section).


##########################![alt=""](.png)</br>##########################

### streamlit dapp

1. Copy deployed `##########################` contract address to SMART_CONTRACT_ADDRESS key in .env file in location of AuctionRegistry dapp. Do the same for `##########################`, but in separate .env file in location of Auction dapp. Locations for each captured in below steps
2. Open command line interface terminal
3. For NFTRegistry dapp, navigate to location ##########################, then input command `##########################`
4. For Auction dapp, navigate to location ##########################, then input command `##########################`

##########################![alt=""](.png)</br>

##########################![alt=""](.png)</br>

##########################![alt=""](.png)</br>

## Video Demos
---


## Outcome and Summary

### NFT Minting
![Minting](screenshot/nft_minting.PNG)

### NFT Transferring with ICO
![Transfer](screenshot/nft_transfer.PNG)


### Optimization and Debugging Opportunities


___


## Contributors
---
Project Team




## References and Resources
---

[OpenZeppelin Contracts Wizard](https://docs.openzeppelin.com/contracts/4.x/wizard) </br>
[OpenZeppelin ERC721 Docs](https://docs.openzeppelin.com/contracts/3.x/api/token/erc721#IERC721-setApprovalForAll-address-bool-)</br>

