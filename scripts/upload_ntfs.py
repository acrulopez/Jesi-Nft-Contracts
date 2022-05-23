from scripts.helpful_scripts import get_account, get_from_config
from brownie import JesiArt


nft_uris = [
    "https://bafybeid5pjo3vevp6sialidxdih27blaxby2zpq4rythlyledmahgkf5a4.ipfs.infura-ipfs.io/",
    "https://bafybeifiumjvkvgohdacnsi75svojpsr2ffjhzwfmjtl7afhzqd25dchha.ipfs.infura-ipfs.io/",
    "https://bafybeiapnejk3ebrwuhfipwjl2h3viofkuatavbaxeaxul4mpl3hne5lxq.ipfs.infura-ipfs.io/",
    "https://bafybeied7y3vu5wi4n64ovb7uvbz5qs2wjqtcdwny73ewikhvurau6ksgy.ipfs.infura-ipfs.io/",
    "https://bafybeif5cw62qceozzv3feuv2bepzhvhltsrykjqum5cnuf466qumajzym.ipfs.infura-ipfs.io/",
    "https://bafybeifrab5ganezvvwliftdeasc4b5u6fpf2yed5xem6mlf7hzw5jifbm.ipfs.infura-ipfs.io/",
    "https://bafybeie726m6rvuaajwmafjkuw4w36akjaw7iheehi3iliozkmf4sl3cqe.ipfs.infura-ipfs.io/",
    "https://bafybeiext5c6rfwt6zdqu2kmvfa6ivhsgpuvd74nk765oxs5ahgau66jky.ipfs.infura-ipfs.io/",
    "https://bafybeiacfhv2hsur6sso7nja64wq5b344otqp4bqg2z5xtfbtg4jcyiz7u.ipfs.infura-ipfs.io/",
    "https://bafybeihxjwd2qxqqp7sxhhhmswcjgrwdx26phdlnwbsizdlkyrlneu7vl4.ipfs.infura-ipfs.io/",
]


def upload_nfts():
    account = get_account()
    jesi_ntf_art = JesiArt[-1]

    for nft_uri in nft_uris:
        jesi_ntf_art.create_ntf(nft_uri, {"from": account})


def main():
    upload_nfts()
