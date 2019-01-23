import hvac
import sys
import argparse


VAULT_URL='http://127.0.0.1:8200'


def show_kv(client, kv_path):
    print('--------------------')
    print('[INFO] Show pair "key: value" for path {path}'.format(
        path=kv_path,
    ))
    kv_data = client.kv.v2.read_secret_version(path=kv_path)['data']['data']
    for item in kv_data:
        print('{key}: {value}'.format(key=item, value=kv_data[item]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', required=True, help='Vault Token')
    parser.add_argument('-e', '--env', required=True, help='Environment')
    args = parser.parse_args()

    client = hvac.Client()
    client = hvac.Client(
        url=VAULT_URL,
        token=args.token
    )

    show_kv(client,"t-systems/cloud_billing/" + args.env + "/application")
    show_kv(client,"t-systems/cloud_billing/" + args.env + "/database")


if __name__ == '__main__':
    sys.exit(main())
