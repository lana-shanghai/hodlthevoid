pragma solidity ^0.6.6;
pragma experimental ABIEncoderV2;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract owned {
    constructor() public { owner = msg.sender; }
    address payable owner;

    // This contract only defines a modifier but does not use
    // it: it will be used in derived contracts.
    // The function body is inserted where the special symbol
    // `_;` in the definition of a modifier appears.
    // This means that if the owner calls this function, the
    // function is executed and otherwise, an exception is
    // thrown.
    modifier onlyOwner {
        require(
            msg.sender == owner,
            "Only owner can call this function."
        );
        _;
    }
}

contract Dogeviathan2 is ERC721, owned {

    uint256 public tokenCounter;
    struct Void {
        uint256 mobility;
        uint256 energy;
        uint256 oxygen;
        uint256 codex;
        uint256 justice;
    }
    mapping(uint256 => Void) public tokenIdToVoid;

    constructor() public
    ERC721("HodlTheVoid", "HTV")
    {
        tokenCounter = 0;
    }
    
    function createCollectible(string memory tokenURI)
    onlyOwner public returns (bytes32)
    {
        uint256 lastTokenId = tokenCounter;
        _safeMint(msg.sender, lastTokenId);
        _setTokenURI(lastTokenId, tokenURI);
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