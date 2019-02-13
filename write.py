import hvac
import sys
import argparse


VAULT_URL='http://127.0.0.1:8200'


#Example function to rewrite kv-entry
def update_kv(client):
    print('[INFO] Update kv example "application" for dev')
    client.secrets.kv.v2.create_or_update_secret(
        path='t-systems/cloud_billing/dev/application',
        secret=dict(
            client_id='dev000-666'
    ))


#Example function to path one key in kv-entry
def patch_kv(client):
    print('[INFO] Path kv example "database" for dev')
    client.secrets.kv.v2.patch(
        path='t-systems/cloud_billing/dev/database',
        secret=dict(
            database='mongo_test_new'
    ))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', required=True, help='Vault Token')
    parser.add_argument('-a', '--action', required=True, help='Action: path or update')
    args = parser.parse_args()

    client = hvac.Client()
    client = hvac.Client(
        url=VAULT_URL,
        token=args.token
    )

    if args.action == 'update':
        update_kv(client)
    elif args.action == 'path':
        patch_kv(client)
    else:
        print('[INFO] Nothing to do')


if __name__ == '__main__':
    sys.exit(main())
