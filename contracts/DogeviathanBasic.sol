pragma solidity ^0.6.6;
pragma experimental ABIEncoderV2;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "./utils/SafeMathOuter.sol";

contract DogeviathanBasic is Ownable, ERC721 {
    using SafeMathOuter for uint256;

    uint256 public tokenCounter;
    uint256 public lastPrice;
    uint256 public constant FIRST_BATCH_SUPPLY = 513;
    uint256 public constant SALE_START_TIMESTAMP = 1617580800; // TODO
    address public constant safe = 0x4B6250BFF504C9B6966d98543dD407315f220345;
    struct Void {
        uint256 mobility;
        uint256 energy;
        uint256 oxygen;
        uint256 codex;
        uint256 justice;
    }
    mapping(uint256 => Void) public tokenIdToVoid;
    mapping(uint256 => address) public tokenIdToOwner;
    mapping(uint256 => uint256) public tokenIdToRand;
    event createdCollectible(uint256 tokenId);

    constructor() public
    ERC721("HodlTheVoid", "HTV")
    {
        tokenCounter = 0;
        lastPrice = 0.01 * 10 ** 18; // initial price is 0.01 ETH
    }
    
    function withdraw() public {
        require(msg.sender == safe);
        uint balance = address(this).balance;
        msg.sender.transfer(balance);
    }

    function getVoidPrice() public view returns (uint256) {
        require(block.timestamp >= SALE_START_TIMESTAMP, "Sale has not started");
        require(tokenCounter < FIRST_BATCH_SUPPLY, "First batch has been sold out");
        return lastPrice;
    }

    function createCollectible()
    public payable returns (uint256)
    {
        require(block.timestamp >= SALE_START_TIMESTAMP, "Sale has not started");
        require(tokenCounter < FIRST_BATCH_SUPPLY, "First batch has been sold out");
        require(getVoidPrice() == msg.value, "Ether value sent is not correct");
        uint256 lastTokenId = tokenCounter;
        address voidOwner = msg.sender;
        if (lastTokenId == FIRST_BATCH_SUPPLY - 1) {
            tokenIdToRand[lastTokenId] = 0;
            tokenIdToVoid[lastTokenId] = indexToVoid(0);
        } else {
            uint256 r = uint(keccak256(abi.encodePacked(voidOwner, msg.value))) % 7776;
            tokenIdToRand[lastTokenId] = r;
            tokenIdToVoid[lastTokenId] = indexToVoid(r);
        }
        _safeMint(voidOwner, lastTokenId);
        lastPrice = lastPrice * 1008 / 1000;
        tokenIdToOwner[lastTokenId] = voidOwner;
        emit createdCollectible(lastTokenId);
        tokenCounter = tokenCounter + 1;
    }

    function indexToVoid(uint256 idx) public returns (Void memory) {
        uint256 r_0 = idx % 1296;
        uint256 a_0 = idx.sub_outer(r_0) / 1296;
        uint256 r_1 = r_0 % 216;
        uint256 a_1 = r_0.sub_outer(r_1) / 216;
        uint256 r_2 = r_1 % 36;
        uint256 a_2 = r_1.sub_outer(r_2) / 36;
        uint256 r_3 = r_2 % 6;
        uint256 a_3 = r_2.sub_outer(r_3) / 6;
        uint256 a_4 = r_3;
        return Void(a_0, a_1, a_2, a_3, a_4);
    }

    function voidToIndex(Void memory void) public returns (uint256) {
        return
            void.justice +
            void.codex.mul_outer(6) +
            void.oxygen.mul_outer(36) +
            void.energy.mul_outer(216) +
            void.mobility.mul_outer(1296);
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) onlyOwner public
    {
        _setTokenURI(tokenId, _tokenURI);
    }

    function burn(uint256 tokenId) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: burn caller is not owner nor approved"
        );
        _burn(tokenId);
        tokenIdToRand[tokenId] = 0;
        tokenIdToVoid[tokenId] = indexToVoid(0);
        tokenIdToOwner[tokenId] = address(0);
    }
}
