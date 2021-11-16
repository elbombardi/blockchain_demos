// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";
import "@chainlink/contracts/src/v0.8/ConfirmedOwner.sol";

contract RandomEAConsumer is ChainlinkClient, ConfirmedOwner {
    using Chainlink for Chainlink.Request;

    uint256 private constant ORACLE_PAYMENT = 100000000000000000;
    uint256[] public randomArray;
    uint256 public randomSize;

    event RequestRandomArrayFulfilled(
        bytes32 indexed requestId,
        uint256[] indexed randomArray
    );

    constructor() ConfirmedOwner(msg.sender) {
        setPublicChainlinkToken();
    }

    function requestRandomArray(
        address _oracle,
        string memory _jobId,
        int256 _size
    ) public onlyOwner {
        Chainlink.Request memory req = buildChainlinkRequest(
            stringToBytes32(_jobId),
            address(this),
            this.fulfillRandomArray.selector
        );
        req.addInt("size", _size);
        sendChainlinkRequestTo(_oracle, req, ORACLE_PAYMENT);
    }

    function fulfillRandomArray(
        bytes32 _requestId,
        uint256[] memory _randomArray
    ) public recordChainlinkFulfillment(_requestId) {
        emit RequestRandomArrayFulfilled(_requestId, _randomArray);
        randomArray = _randomArray;
        randomSize = _randomArray.length;
    }

    function getChainlinkToken() public view returns (address) {
        return chainlinkTokenAddress();
    }

    function withdrawLink() public onlyOwner {
        LinkTokenInterface link = LinkTokenInterface(chainlinkTokenAddress());
        require(
            link.transfer(msg.sender, link.balanceOf(address(this))),
            "Unable to transfer"
        );
    }

    function cancelRequest(
        bytes32 _requestId,
        uint256 _payment,
        bytes4 _callbackFunctionId,
        uint256 _expiration
    ) public onlyOwner {
        cancelChainlinkRequest(
            _requestId,
            _payment,
            _callbackFunctionId,
            _expiration
        );
    }

    function stringToBytes32(string memory source)
        private
        pure
        returns (bytes32 result)
    {
        bytes memory tempEmptyStringTest = bytes(source);
        if (tempEmptyStringTest.length == 0) {
            return 0x0;
        }

        assembly {
            // solhint-disable-line no-inline-assembly
            result := mload(add(source, 32))
        }
    }
}
