// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";
import "@openzeppelin/contracts/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin/contracts/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

import "./Collection.sol";

contract CollectionManager is
    Initializable,
    UUPSUpgradeable,
    Ownable,
    AccessControl
{
    bytes32 public constant CREATOR_ROLE = keccak256("CREATOR_ROLE");

    address payable[] public collections;
    address public collectionImplementation;
    mapping(string => bool) public isContractUriCreated;

    event CollectionCreated(address collection);

    function createCollection(
        string memory _name,
        string memory _token,
        string memory _contractURI,
        uint256 _maxSupply,
        uint256 _mintFee
    ) public onlyRole(CREATOR_ROLE) returns (address) {
        require(
            !isContractUriCreated[_contractURI],
            "This IPFS hash has already been added to a collection."
        );

        bytes memory initializeData = abi.encodeWithSelector(
            Collection.initialize.selector,
            _name,
            _token,
            _contractURI,
            _maxSupply,
            _mintFee
        );

        ERC1967Proxy newCollection = new ERC1967Proxy(
            collectionImplementation,
            initializeData
        );
        collections.push(payable(newCollection));
        isContractUriCreated[_contractURI] = true;
        emit CollectionCreated(address(newCollection));
        return address(newCollection);
    }

    function initialize(address _collectionImplementation, address creator)
        public
        initializer
    {
        collectionImplementation = _collectionImplementation;
        _transferOwnership(_msgSender());
        _setupRole(CREATOR_ROLE, _msgSender());
        _setupRole(CREATOR_ROLE, creator);
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
