# vault-demo

## Start Vault
For this example we will run Vault in dev mode.

First of all download latest version of [Vault](https://www.vaultproject.io/downloads.html)

To start the Vault dev server, run:

`vault server -dev`

## Initialize Vault with test data

Run command in console:

`python init.py -t <token>`

## Create new tokens

Open new console and export Vault address:

`export VAULT_ADDR='http://127.0.0.1:8200'`

Login to vault with root token and generate another token:

`vault token create`

Use this new token to login to Web UI

## Examples

1. Read kv from Vault

1.a. Standard situation

Generate token for read-only access:

`vault token create -policy=my-policy-read`

Test scripts:

`python read.py -e dev -t <token>`

`python read.py -e prod -t <token>`

1.b. Restricted access:

Generate token for restricted access:

`vault token create -policy=my-policy-secure`

Test scripts - from 1.a.

1.c. One-time password

Generate token for restricted access:

`vault token create -policy=my-policy-read -use-limit=1`

Test scripts - run first script from 1.a. twice

2. Write kv to Vault

Generate token with write access to dev environment:

`vault token create -policy=my-policy-dev`

Test scripts:

`python write.py -a update -t <token>`

`python write.py -a path -t <token>`
