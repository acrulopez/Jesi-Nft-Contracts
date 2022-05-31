// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/proxy/utils/Initializable.sol";

contract Collection is ERC721URIStorage, Initializable {
    string private __name;
    string private __symbol;
    string public collectionURI;
    uint256 public totalSupply;
    uint256 public maxTotalSupply;

    constructor(
        string memory _name,
        string memory _token,
        uint256 _maxTotalSupply,
        string memory _collectionURI
    ) ERC721(_name, _token) {
        __name = _name;
        __symbol = _token;
        collectionURI = _collectionURI;
        maxTotalSupply = _maxTotalSupply;
    }

    function initialize(
        string memory _name,
        string memory _token,
        uint256 _maxTotalSupply,
        string memory _collectionURI
    ) public initializer {
        __name = _name;
        __symbol = _token;
        collectionURI = _collectionURI;
        maxTotalSupply = _maxTotalSupply;
    }

    function name() public view override returns (string memory) {
        return __name;
    }

    function symbol() public view override returns (string memory) {
        return __symbol;
    }

    function mint(address _nftOwner, string memory _tokenURI)
        public
        returns (uint256)
    {
        require(totalSupply < maxTotalSupply);
        uint256 tokenId = totalSupply;
        _mint(_nftOwner, tokenId);
        _setTokenURI(tokenId, _tokenURI);
        totalSupply = totalSupply + 1;
        return tokenId;
    }

    function burn(uint256 tokenId) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "Collection: only owner or approved can burn a token"
        );
        _burn(tokenId);
        totalSupply -= 1;
    }
}
