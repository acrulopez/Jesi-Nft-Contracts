// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract UpgradedCollection is ERC721URIStorage, Initializable, Ownable {
    string private __name;
    string private __symbol;
    string public collectionURI;
    uint256 public totalSupply;
    uint256 public maxTotalSupply;
    uint256 mintFee;
    uint256 public foo;

    constructor(
        string memory _name,
        string memory _token,
        uint256 _maxTotalSupply,
        string memory _collectionURI,
        uint256 _mintFee
    ) ERC721(_name, _token) {
        __name = _name;
        __symbol = _token;
        collectionURI = _collectionURI;
        maxTotalSupply = _maxTotalSupply;
        mintFee = _mintFee;
    }

    function initialize(
        string memory _name,
        string memory _token,
        uint256 _maxTotalSupply,
        string memory _collectionURI,
        uint256 _mintFee
    ) public initializer {
        __name = _name;
        __symbol = _token;
        collectionURI = _collectionURI;
        maxTotalSupply = _maxTotalSupply;
        mintFee = _mintFee;
        _transferOwnership(_msgSender());
    }

    function name() public view override returns (string memory) {
        return __name;
    }

    function symbol() public view override returns (string memory) {
        return __symbol;
    }

    function setFoo(uint256 _foo) public {
        foo = _foo;
    }

    function mint(address _nftOwner, string memory _tokenURI)
        public
        payable
        returns (uint256)
    {
        require(totalSupply < maxTotalSupply);
        require(msg.value >= mintFee);
        uint256 tokenId = totalSupply;
        _mint(_nftOwner, tokenId);
        _setTokenURI(tokenId, _tokenURI);
        ++totalSupply;
        return tokenId;
    }

    function burn(uint256 tokenId) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "Collection: only owner or approved can burn a token"
        );
        _burn(tokenId);
        --totalSupply;
    }

    function withdraw() public payable onlyOwner {
        payable(msg.sender).transfer(address(this).balance);
    }
}

// uint256 public foo;

// function setFoo(uint256 _foo) public {
//     foo = _foo;
// }
