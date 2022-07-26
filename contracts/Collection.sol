// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin/contracts/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/utils/Address.sol";

contract Collection is
    ERC721URIStorage,
    Initializable,
    UUPSUpgradeable,
    Ownable
{
    string private __name;
    string private __symbol;
    string public contractURI;
    uint256 public maxSupply;
    uint256 public mintFee;
    uint256 public totalSupply;

    constructor() ERC721("", "") {}

    function initialize(
        string memory _name,
        string memory _token,
        string memory _contractURI,
        uint256 _maxSupply,
        uint256 _mintFee
    ) public initializer {
        __name = _name;
        __symbol = _token;
        contractURI = _contractURI;
        maxSupply = _maxSupply;
        mintFee = _mintFee;
        _transferOwnership(_msgSender());
    }

    function name() public view override returns (string memory) {
        return __name;
    }

    function symbol() public view override returns (string memory) {
        return __symbol;
    }

    function mint(address _tokenOwner, string memory _tokenURI)
        public
        payable
        returns (uint256)
    {
        require(
            totalSupply < maxSupply,
            "This collection has reached its maximum tokens"
        );
        require(
            msg.value == mintFee,
            "Please send exactly the minting fee of this collection."
        );
        Address.sendValue(payable(owner()), address(this).balance);
        uint256 tokenId = totalSupply;
        _mint(_tokenOwner, tokenId);
        _setTokenURI(tokenId, _tokenURI);
        ++totalSupply;
        return tokenId;
    }

    function _authorizeUpgrade(address newImplementation)
        internal
        override
        onlyOwner
    {}

    function withdraw() public onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }

    receive() external payable {}
}
