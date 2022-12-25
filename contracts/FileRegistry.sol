pragma solidity ^0.5.5;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract FileRegistry is ERC721Full {
    constructor() public ERC721Full("FileRegistryToken", "FILE") {}

    struct File {
        string name;
        string fileOwner;
    }

    mapping(uint256 => File) public folder;

    function registerFile(address owner, string memory name, string memory fileOwner, string memory tokenURI) public returns (uint256) {
        uint256 tokenId = totalSupply();
        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);
        folder[tokenId] = File(name, fileOwner);
        return tokenId;
    }
}


/*
Register art/file

    tokenid = contract.functions.registerFile(owner_address, name_of_file, name_of_owner, tokenURI).transact({"from": owner_address, "gas": 100000})

Transfer owner

    contract.functions.transferFrom(owner_address, purchaser_address, tokenid).transact({"from": owner_address, "gas": 100000})

Display owner of the specific tokenid

    contract.functions.ownerOf(tokenid).transact({"from": owner_address, "gas": 100000})

Display token URI

    contract.functions.tokenURI(tokenid).transact({"from": owner_address, "gas": 100000})
*/
