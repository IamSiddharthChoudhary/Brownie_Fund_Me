// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract Funds {
    //When mapping is initialised all the keys are initialised.
    mapping(address => uint256) public fundsArray;
    address[] public funders;
    address public owner;
    AggregatorV3Interface public Aggregator;

    constructor(address priceFeed) public {
        Aggregator = AggregatorV3Interface(priceFeed);
        //This msg.sender is no one but the address from which the contract was deployed/called first.
        owner = msg.sender;
    }

    function fund() public payable {
        uint256 minValueUsd = 1 * 10**18;
        require(
            convertToUsd(msg.value) >= minValueUsd,
            "Veer g paise ghat je!"
        );
        fundsArray[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        return Aggregator.version();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = Aggregator.latestRoundData();
        return uint256(answer * 10000000000); // for getting answer in 18 decimals.
    }

    function convertToUsd(uint256 ethAmount) public view returns (uint256) {
        uint256 currentPrice = getPrice();
        uint256 finalValue = (currentPrice * ethAmount) / (10**18);
        return finalValue;
    }

    function getEntraceFees() public view returns (uint256) {
        uint256 minimumUSD = 50 + 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (minimumUSD * precision) / price;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Chor kahin ka");
        _;
    }

    function withdraw() public payable onlyOwner {
        // So that only the ower could withdraw the ammount
        //require(msg.sender == owner, "Chor kahin ke");  but we have an another way of doing it too
        // i.e. by modifiers.
        payable(msg.sender).transfer(address(this).balance);
        for (
            uint80 funderIndex = 0;
            funderIndex > funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            fundsArray[funder] = 0;
        }
        funders = new address[](0);
    }
}
