vault server -dev

#########################

export VAULT_ADDR='http://127.0.0.1:8200'

#########################

vault login

write account:
vault token create -policy=my-policy-write

read only account:
vault token create -policy=my-policy-read

dev account:
vault token create -policy=my-policy-read -policy=my-policy-dev

secure account:
vault token create -policy=my-policy-secure

token with limits:
vault token create -policy=my-policy-read -use-limit=4
