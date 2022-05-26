// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/proxy/utils/Initializable.sol";

contract JesiArt is ERC721URIStorage, Initializable {
    string private __name;
    string private __symbol;
    uint256 public tokenCounter;
    uint256 public maxTokens;

    constructor(
        string memory _name,
        string memory _token,
        uint256 _maxTokens
    ) ERC721(_name, _token) {
        __name = _name;
        __symbol = _token;
        maxTokens = _maxTokens;
    }

    function initialize(
        string memory _name,
        string memory _token,
        uint256 _maxTokens
    ) public initializer {
        __name = _name;
        __symbol = _token;
        maxTokens = _maxTokens;
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
