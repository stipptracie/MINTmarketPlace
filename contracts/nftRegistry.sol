// SPDX-License-Identifier: MIT
pragma solidity ^0.5.2;
import "https://github.com/athiwatp/openzeppelin-solidity/blob/master/contracts/token/ERC721/ERC721Full.sol";

contract MyNFT is ERC721Full {
    address payable owner;

    // naming the token, "FileToken" for each individual uploaded file
    constructor() public ERC721Full("FileToken", "FLT") {}

    modifier onlyOwner {
    require(msg.sender == owner, "You do not have permission to mint these tokens!");
    _;
    }

    // function for user to register/mint artwork with unique token
    function mint(address recipient, string memory tokenURI) public onlyOwner returns(uint256) {        
        
        uint256 tokenId = totalSupply();
        _mint(recipient, tokenId);
        _setTokenURI(tokenId, tokenURI);

        return tokenId;        
    }
}