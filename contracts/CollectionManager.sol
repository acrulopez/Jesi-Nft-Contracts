// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";
import "@openzeppelin/contracts/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin/contracts/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "./Collection.sol";

contract CollectionManager is Initializable, UUPSUpgradeable, Ownable {
    address payable[] public collections;
    address public collectionImplementation;

    function createCollection(
        string memory _name,
        string memory _token,
        string memory _description,
        string memory _ipfsHash,
        uint256 _maxTotalSupply,
        uint256 _mintFee
    ) public returns (address) {
        bytes memory initializeData = abi.encodeWithSelector(
            Collection.initialize.selector,
            _name,
            _token,
            _description,
            _ipfsHash,
            _maxTotalSupply,
            _mintFee
        );

        ERC1967Proxy newCollection = new ERC1967Proxy(
            collectionImplementation,
            initializeData
        );
        collections.push(payable(newCollection));
        return address(newCollection);
    }

    function initialize(address _collectionImplementation) public initializer {
        collectionImplementation = _collectionImplementation;
        _transferOwnership(_msgSender());
    }

    function upgradeAllCollectionImplementation(address newImplementation)
        public
    {
        unchecked {
            for (uint256 i; i < collections.length; ++i) {
                upgradeCollectionImplementation(i, newImplementation);
            }
        }
    }

    function upgradeCollectionImplementation(
        uint256 collectionIndex,
        address newImplementation
    ) public onlyOwner {
        Collection(collections[collectionIndex]).upgradeTo(newImplementation);
    }

    function _authorizeUpgrade(address newImplementation)
        internal
        override
        onlyOwner
    {}

    function withdraw() public onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }

    function withdrawFrom(uint256 collectionIndex) public onlyOwner {
        Collection(collections[collectionIndex]).withdraw();
    }

    receive() external payable {}
}
