pragma solidity ^0.5.5;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Detailed.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Mintable.sol";

contract InAppCoin is ERC20, ERC20Detailed, ERC20Mintable {
    constructor(uint initial_suppy) ERC20Detailed("InAppCoin", "IAPC", 18) public {
        mint(msg.sender, initial_suppy);
    }
}

/* ERC20 includes transfer function
For coin offering from the website to pertifipant

    contract.function.transfer(purchaser_address/seller_address, offer_amount).transact({"from": owner_address, "gas": 100000})

For coin transfer from purchaser to buyer

    contract.function.Approve(owner_address, NFT_price).transact({"from": purchaser_address, "gas": 100000})
    contract.function.transferFrom(purchaser_address, seller_address, NFT_price).transact({"from":owner_address, "gas":100000})
    contract.function.decreaseAllowance(owner_address, NFT_price).transact({"from": purchaser_address, "gas": 100000})
OR
    contract.function.transfer(seller_address, NFT_price).transact({"from":purchaser_address, "gas": 100000})
*/