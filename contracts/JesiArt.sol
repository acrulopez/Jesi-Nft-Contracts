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

    function mint(address _nftOwner, string memory _tokenURI) public {
        require(tokenCounter <= maxTokens);
        _mint(_nftOwner, tokenCounter);
        _setTokenURI(tokenCounter, _tokenURI);
        tokenCounter = tokenCounter + 1;
    }
}
