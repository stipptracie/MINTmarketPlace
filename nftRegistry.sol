// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/access/Ownable.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract MyNFT is Ownable, ERC721URIStorage {      
    // name and symbol
    constructor() ERC721("__________", "______") {
    }
    function mint(address recipient, uint256 tokenId, 
    string memory tokenURI) public onlyOwner {        
        _mint(recipient, tokenId);
        _setTokenURI(tokenId, tokenURI);        
    }
}