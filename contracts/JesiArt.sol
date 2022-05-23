// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract JesiArt is ERC721URIStorage {
    uint256 public tokenCounter;

    constructor(string memory _name, string memory _token)
        ERC721(_name, _token)
    {}

    function create_ntf(string memory _tokenURI) public {
        _mint(msg.sender, tokenCounter);
        _setTokenURI(tokenCounter, _tokenURI);
        tokenCounter = tokenCounter + 1;
    }
}
