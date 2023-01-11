pragma solidity ^0.5.5;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract MintRegistry is ERC721Full {
    // naming the token, "FileToken" for each individual uploaded file
    constructor() public ERC721Full("FileToken", "FILE") {}

    // function for user to register/mint artwork with unique token
    function registerFile(address owner, string memory tokenURI)
        public
        returns (uint256)
    {
        uint256 tokenId = totalSupply();
        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);

        return tokenId;
    }
}