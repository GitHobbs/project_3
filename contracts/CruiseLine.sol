/// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract CruiseLine is ERC1155, Ownable {
    using Counters for Counters.Counter;

    Counters.Counter private _tokenIds;
    Counters.Counter private _sailingIds;

    // Mapping to keep track of balances
    mapping(uint256 => mapping(address => uint256)) private _balances;

    // Mapping to store cabin details
    mapping(uint256 => Cabin) private _cabins;

    // Mapping to store sailing details
    mapping(uint256 => Sailing) private _sailings;

    // Mapping to track tokens minted by tokenId
    mapping(uint256 => uint256) private _cabinsMinted;

    // Struct to represent a sailing
    struct Sailing {
        uint256 sailingId;
        uint256 departureDate;
        uint256 numberOfNights;
        string shipName;
    }

    // Struct to represent a cabin
    struct Cabin {
        uint256 price;
        uint256 availability;
        string cabinType;
    }

    event CabinMinted(
        uint256 indexed tokenId,
        address indexed account,
        uint256 quantity
    );

    event CabinTransfer(
        address indexed from,
        address indexed to,
        uint256 indexed tokenId,
        uint256 quantity
    );

    event CabinAvailabilityUpdated(
        uint256 indexed tokenId,
        uint256 newAvailability
    );

    event SailingCreated(
        uint256 indexed sailingId,
        uint256 departureDate,
        uint256 numberOfNights,
        string shipName
    );

    event CabinCreated(
        uint256 indexed tokenId,
        uint256 price,
        uint256 initialAvailability,
        string cabinType
    );

    event Log(
        string 
    );

    event LogNumber(uint);
    
    event Sailings (
          uint256 sailingId,
        uint256 departureDate,
        uint256 numberOfNights,
        string shipName
    );


    event ContractBalanceWithdrawn(address indexed owner, uint256 amount);

    // Mapping to associate cabin tokens with their respective sailing IDs
    mapping(uint256 => Sailing) private _cabinSailing;

    constructor() ERC1155("127.0.0.1:8545") {
        // Pass an empty URI string for token metadata
        // You can replace it with the base URI for your tokens
    }

    // Function to create a new sailing
    function createSailing(
        uint256 departureDate,
        uint256 numberOfNights,
        string memory shipName
    ) external returns (uint256) {
        // Increment the token ID counter
        _sailingIds.increment();

        uint256 newSailingId = _sailingIds.current();

        // Create a new sailing
        _sailings[newSailingId] = Sailing(
            newSailingId,
            departureDate,
            numberOfNights,
            shipName
        );

        emit SailingCreated(
            newSailingId,
            departureDate,
            numberOfNights,
            shipName
        );

        return newSailingId;
    }

    // Function to create a new cabin type
    function createCabin(
        uint256 price,
        uint256 initialAvailability,
        string memory cabinType,
        uint256 sailingId
    ) external returns (uint256) {
        uint256 newTokenId = _tokenIds.current();

        // Create a new cabin
        _cabins[newTokenId] = Cabin(price, initialAvailability, cabinType);

        // Fetch the sailing details
        Sailing storage sailing = _sailings[sailingId];

        // Associate the cabin token with the sailing details
        _cabinSailing[newTokenId] = sailing;

        // Add cabin to the cabinsMinted mapping and set equal to 0
        _cabinsMinted[newTokenId] = 0;

        // Increment the token ID counter
        _tokenIds.increment();

        emit CabinCreated(newTokenId, price, initialAvailability, cabinType);

        return newTokenId;
    }

    // Function to mint new cabin tokens
    function mintCabin(uint256 tokenId, uint256 amount) external payable {
        address account = msg.sender;
        // Check if there are enough cabins available
        require(
            _cabins[tokenId].availability >= amount,
            "Insufficient availability"
        );

        // Check if the sent amount matches the required price
        require(
            msg.value == _cabins[tokenId].price * amount,
            "Incorrect amount sent"
        );

        // Mint the new cabin tokens
        _mint(account, tokenId, amount, "");

        // Update the balances
        _balances[tokenId][account] += amount;

        // Update the availability
        _cabins[tokenId].availability -= amount;

        // Track the minted tokens in the mapping
        _cabinsMinted[tokenId] += amount;

        emit CabinMinted(tokenId, account, amount);
        emit CabinAvailabilityUpdated(tokenId, _cabins[tokenId].availability);
    }

    // Function to get the cabin details for a token ID
    function getCabin(uint256 tokenId) external view returns (Cabin memory) {
        return _cabins[tokenId];
    }

    // Function to get the sailing associated with a cabin token
    function getCabinSailing(uint256 tokenId)
        external
        view
        returns (Sailing memory)
    {
        return _cabinSailing[tokenId];
    }

    // Function to get the sailing associated with a sailing ID
    function getSailing(uint256 sailingId)
        external
        view
        returns (Sailing memory)
    {
    
        return _sailings[sailingId];
    }

    // Function to get the balance of a specific cabin type for an address
    function balanceOfCabin(address account, uint256 tokenId)
        external
        view
        returns (uint256)
    {
        return _balances[tokenId][account];
    }

    // Function to transfer cabin tokens from the caller's address to another address
    function transferCabin(
        address to,
        uint256 tokenId,
        uint256 amount
    ) external {
        address from = msg.sender;
        // Check if the caller owns enough cabin tokens
        require(_balances[tokenId][from] >= amount, "Insufficient balance");

        // Update the balances
        _balances[tokenId][from] -= amount;
        _balances[tokenId][to] += amount;

        // Transfer the cabin tokens
        _safeTransferFrom(from, to, tokenId, amount, "");
    }

    // Function to withdraw the contract balance to the owner's account
    function withdrawBalance() external onlyOwner {
        uint256 contractBalance = address(this).balance;
        require(contractBalance > 0, "No balance to withdraw");

        address payable owner = payable(owner());
        owner.transfer(contractBalance);
    }

    // Function to update the availability of a cabin
    function updateCabinAvailability(uint256 tokenId, uint256 newAvailability)
        external
        onlyOwner
    {
        _cabins[tokenId].availability = newAvailability;
    }

    //Function to retrieve availability for a particular tokenId
    function getAvailability(uint256 tokenId) external view returns (uint256) {
        return _cabins[tokenId].availability;
    }

    //Function to get contract balance
    function getContractBalance() external view returns (uint256) {
        return address(this).balance;
    }


    function getSailingCount () external view returns (uint256){
        return _sailingIds.current();
    }

    function getAllSailings() external view returns (Sailing[] memory){
         uint256 totalSailings = _sailingIds.current();
        Sailing[] memory sailings = new Sailing[](totalSailings);
        
        for (uint256 i = 0; i < totalSailings; i++) {
            sailings[i] = _sailings[i];
        }
        
        return sailings;
    }
    
}
