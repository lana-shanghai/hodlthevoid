pragma solidity ^0.6.6;
pragma experimental ABIEncoderV2;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Dogeviathan is Ownable, ERC721, VRFConsumerBase {

    bytes32 internal keyHash;
    uint256 public fee;
    uint256 public tokenCounter;
    uint256 public lastPrice;
    uint256 public rand;
    uint256 public constant FIRST_BATCH_SUPPLY = 513;
    uint256 public constant SALE_START_TIMESTAMP = 1617580800; // TODO
    struct Void {
        uint256 mobility;
        uint256 energy;
        uint256 oxygen;
        uint256 codex;
        uint256 justice;
    }
    mapping(bytes32 => address) public requestIdToSender;
    mapping(bytes32 => string) public requestIdToTokenURI;
    mapping(uint256 => Void) public tokenIdToVoid;
    mapping(uint256 => uint256) public tokenIdToRand;
    mapping(bytes32 => uint256) public requestIdToTokenId;
    event requestedCollectible(bytes32 indexed requestId);

    constructor(address _VRFCoordinator, address _LinkToken, bytes32 _keyhash) public
    VRFConsumerBase(_VRFCoordinator, _LinkToken)
    ERC721("HodlTheVoid", "HTV")
    {
        keyHash = _keyhash;
        fee = 0.1 * 10 ** 18; // 0.1 LINK
        tokenCounter = 0;
        lastPrice = 0.01 * 10 ** 18; // initial price is 0.01 ETH
    }
    
    function withdraw() onlyOwner public {
        uint balance = address(this).balance;
        msg.sender.transfer(balance);
    }

    function getVoidPrice() public view returns (uint256) {
        require(block.timestamp >= SALE_START_TIMESTAMP, "Sale has not started");
        require(tokenCounter < FIRST_BATCH_SUPPLY, "First batch has been sold out");
        return lastPrice;
    }

    function createCollectible(string memory tokenURI)
    public payable returns (bytes32) 
    {
        require(block.timestamp >= SALE_START_TIMESTAMP, "Sale has not started");
        require(tokenCounter < FIRST_BATCH_SUPPLY, "First batch has been sold out");
        require(getVoidPrice() == msg.value, "Ether value sent is not correct");
        lastPrice = lastPrice * 1008 / 1000;
        bytes32 requestId = requestRandomness(keyHash, fee);
        requestIdToSender[requestId] = msg.sender;
        requestIdToTokenURI[requestId] = tokenURI;
        emit requestedCollectible(requestId);
    }

    function indexToVoid(uint256 idx) public returns (Void memory) {
        uint256 r_0 = idx % 1296;
        uint256 a_0 = (idx - r_0) / 1296; // TODO replace with sub
        uint256 r_1 = r_0 % 216;
        uint256 a_1 = (r_0 - r_1) / 216;
        uint256 r_2 = r_1 % 36;
        uint256 a_2 = (r_1 - r_2) / 36;
        uint256 r_3 = r_2 % 6;
        uint256 a_3 = (r_2 - r_3) / 6;
        uint256 a_4 = r_3;
        return Void(a_0, a_1, a_2, a_3, a_4);   
    }

    function voidToIndex(Void memory void) public returns (uint256) {
        return 
            void.justice + // TODO replace with add and mul
            void.codex * 6 + 
            void.oxygen * 36 + 
            void.energy * 216 + 
            void.mobility * 1296;
    }

    function randToVoid(uint256 r) public returns (Void memory) {
        Void memory newVoid = indexToVoid(r);
        return newVoid;
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
    internal override
    {
       address voidOwner = requestIdToSender[requestId];
       string memory tokenURI = requestIdToTokenURI[requestId];
       uint256 lastTokenId = tokenCounter;
       _safeMint(voidOwner, lastTokenId);
       _setTokenURI(lastTokenId, tokenURI);
       rand = randomNumber % 7776;
       tokenIdToRand[lastTokenId] = rand;
       tokenIdToVoid[lastTokenId] = indexToVoid(rand);
       requestIdToTokenId[requestId] = lastTokenId;
       tokenCounter = tokenCounter + 1;

    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public 
    {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: transfer caller is not owner nor approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }

}