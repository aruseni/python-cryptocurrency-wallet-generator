# Python cryptocurrency wallet generator

This is a simple Python package for generating wallets for several cryptocurrencies.

Currently supported cryptocurrencies:

* Bitcoin
* Bitcoin Cash
* Dash
* Ethereum
* Litecoin

## Install

    pip install cryptocurrency-wallet-generator

## Usage

    from cryptocurrency_wallet_generator import generate_wallet

    private_key, address = generate_wallet("Bitcoin")

You can also use the generate_wallet method of a particular currency class directly.

    from cryptocurrency_wallet_generator.currencies.bitcoin import Bitcoin

    currency = Bitcoin()
    private_key, address = currency.generate_wallet()

The `generate_wallet` function returns a tuple that contains a private key and the corresponding address.
