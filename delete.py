import hvac
import sys
import argparse


VAULT_URL='http://127.0.0.1:8200'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', required=True, help='Vault Token')
    parser.add_argument('-v', '--version', required=True, help='Version')
    args = parser.parse_args()

    client = hvac.Client()
    client = hvac.Client(
        url=VAULT_URL,
        token=args.token
    )

    kv_path='t-systems/cloud_billing/dev/database'
    secret_version_response = client.secrets.kv.v2.read_secret_version(
        path=kv_path)

    latest_version=secret_version_response['data']['metadata']['version']
    print('[INFO] Latest version is #{ver}'.format(
        ver=latest_version
    ))

    print('[INFO] Delete latest version')
    client.secrets.kv.v2.delete_latest_version_of_secret(
        path=kv_path
        )

    print('[INFO] Previous version')
    kv_data_prev = client.kv.v2.read_secret_version(
        path=kv_path,
        version=latest_version-1
    )
    for item in kv_data_prev['data']['data']:
        print('{key}: {value}'.format(
            key=item,
            value=kv_data_prev['data']['data'][item]
    ))

    print('[INFO] Rollback to previous version')
    client.secrets.kv.v2.create_or_update_secret(
        path=kv_path,
        secret=kv_data_prev['data']['data']
    )


if __name__ == '__main__':
    sys.exit(main())
