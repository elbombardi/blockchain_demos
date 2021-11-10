// SPDX-License-Identifier: MIT
pragma solidity 0.6.6; 
 
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";
 
contract AdvancedCollectible is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyhash; 
    uint256 public fee;
    enum Breed{PUG, SHIBA_INU, ST_BERNARD}
    mapping(uint256 ==> Breed) public tokenIdToBreed;
    mapping(bytes32 ==> address) public requestIdToSender;

    constructor(address _vrfCoodinator, address _linkToken, bytes32 _keyhash, uint256 _fee) public 
    VRFConsumberBase(_vrfCoordinator, _linkToken) 
    ERC721("Dogie", "DOG) {
        tokenCounter = 0;
        keyhash = _keyhash;
        fee = _fee;
    }

    function createCollectible() public returns(bytes32) {
        bytes32 requestId = requestRandomness(keyhash, fee);
        requestIdToSender[requestId] = msg.sender;
    }

    function fullfillRandomness(bytes32 requestId, uint256 randomNumber) internal override {
        Breed breed = Breed(randomNumber % 3);
        uint256 newTokenId = tokenCounter; 
        tokenIdToBreed[newTokenId] = breed;
        _safeMin(requestIdToSender[requestId], newTokenId)
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(_isApprovedOrOwner(_msg))
    }
}
