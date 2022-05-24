// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract JesiArt is ERC721URIStorage {
    uint256 public tokenCounter;
    uint256 public maxTokens;

    constructor(
        string memory _name,
        string memory _token,
        uint256 _maxTokens
    ) ERC721(_name, _token) {
        maxTokens = _maxTokens;
    }

    function mint(address _nftOwner, string memory _tokenURI)
        public
        returns (uint256)
    {
        require(tokenCounter < maxTokens);
        uint256 tokenId = tokenCounter;
        _mint(_nftOwner, tokenId);
        _setTokenURI(tokenId, _tokenURI);
        tokenCounter = tokenCounter + 1;
        return tokenId;
    }

    function burn(uint256 tokenId) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "JesiArt: only owner or approved can burn a token"
        );
        _burn(tokenId);
        tokenCounter -= 1;
    }
}
