import hvac
import sys
import argparse


VAULT_URL='http://127.0.0.1:8200'


def write_kv(client):
    print('[INFO] Update kv example for dev')
    client.secrets.kv.v2.create_or_update_secret(
        path='t-systems/cloud_billing/dev/application',
        secret=dict(
            client_id='dev000-666'
    ))


def patch_kv(client):
    print('[INFO] Path kv example for dev')
    client.secrets.kv.v2.patch(
        path='t-systems/cloud_billing/dev/database',
        secret=dict(
            database='mongo_test_new'
    ))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', required=True, help='Vault Token')
    args = parser.parse_args()

    client = hvac.Client()
    client = hvac.Client(
        url=VAULT_URL,
        token=args.token
    )

    write_kv(client)
    patch_kv(client)


if __name__ == '__main__':
    sys.exit(main())
