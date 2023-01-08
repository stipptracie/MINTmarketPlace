// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";


// Inherit OpenZeppelin and ChainLink contracts
// OpenZeppelin ERC721 is standards contract
// OpenZeppelin ERC721URIStorage is a URI storage contract
// OpenZeppelin Ownable is an access control contract which limits functionality to OnlyOwner

contract AuctionRegistry is ERC721, ERC721URIStorage, Ownable {

    //Calling Counters contract function for _tokenIdCounter
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIdCounter;
    address contractAddress;

// Create contructor to link this contract with the auction contract
    constructor(address auctionAddress) ERC721("AuctionRegistry", "AUT") {
        contractAddress = auctionAddress;
    }

// Define NFT data structure
    struct NFT {
        address owner;
        string name;
        string creator;
        string uri;
    }

// Map AuctionCollection for NFT details
    mapping(uint256 => NFT) public AuctionCollection;

// Create registerNFT contract where only contract deployer may register NFTs
    function registerNFT(
        address owner,
        string memory name,
        string memory creator,
        string memory uri
    ) public onlyOwner returns (uint256) {

        // Use Counters to track tokenIDs
        uint256 tokenId = _tokenIdCounter.current();

        // Increment token IDs
        _tokenIdCounter.increment();

        // Mint NFT
        _safeMint(owner, tokenId);

        // Set token URI
        _setTokenURI(tokenId, uri);

        // Add tokenID to AuctionCollection
        AuctionCollection[tokenId] = NFT(owner, name, creator, uri);

        // Return registered NFT tokenId
        return tokenId;

    }

    // The following functions are overrides required by Solidity.

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }
}

