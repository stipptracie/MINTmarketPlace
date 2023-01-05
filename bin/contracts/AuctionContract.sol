pragma solidity ^0.8.10;

contract Auction {
    // Set events for start, end and bid to record on the blockchain
    event Start();
    event End(address highestBidder, uint highestBid);
    event Bid(address indexed sender, uint amount);

    // Set variables for later use
    address public store;
    bool public started;
    bool public ended;
    uint public endAt;
    uint public highestBid;
    address public highestBidder;

    // Create mapping/dictionary to save bids
    mapping(address => uint) public bids;

    // Initialize/set store variable
    constructor() {
        store = msg.sender;
    }

    // Start auction
    function start(uint startingBid) external {
        // Check if the auction is started by the website owner
        require(!started, "Already started.");
        require(msg.sender == store, "You are not authorized.");
        started = true;
        endAt = block.timestamp + 3 minutes; // AUCTION TIME SET AS 3 MINUTES FOR DEVELOPING PURPOSE
        highestBid = startingBid;
        
        // Record this event on blockchain
        emit Start();
    }

    // Bid
    function bid(uint amount) external {
        // Check if the auction is alive and amount offered is greater than the starting price
        require(started, "Not started.");
        require(block.timestamp < endAt, "Ended.");
        require(amount > highestBid);

        // Save new bidder in the mapping/dictionary
        if (highestBidder != address(0)) {
            bids[highestBidder] += highestBid;
        }
        highestBid = amount;
        highestBidder = msg.sender;

        // Record this event on blockchain
        emit Bid(highestBidder, highestBid);
    }

    // End auction
    function end() external {
        // Check if the auction is ended by the website owner
        require(msg.sender == store, "You are not authorized.");
        // Check if the auction exists and pre-set ending time is met
        require(started, "Auction does not exist.");
        require(block.timestamp >= endAt, "Auction has not ended.");
        require(!ended, "Auction has ended.");
        ended = true;

        // Record this event on blockchain
        emit End(highestBidder, highestBid);
    }
}

/*
Start Auction

    contract.functions.start(starting_price).transact({"from": store_address, "gas": 100000})

Accept Bids

    contract.functions.bid(amount).transact({"from": bidder_address, "gas": 100000})

Show Current Price

    contract.functions.highestBid().call()

Show Current Winner

    contract.functions.highestBidder().call()

Show Auction End Time

    contract.functions.endAt().call()

End Auction

    contract.fuctions.end().transact({"from": store_address, "gas": 100000})
*/