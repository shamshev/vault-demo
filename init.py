import hvac
import sys
import argparse


VAULT_URL='http://127.0.0.1:8200'


def create_kv(client):
    print('[INFO] Create kv example for dev')
    client.secrets.kv.v2.create_or_update_secret(
        path='t-systems/cloud_billing/dev/database',
        secret=dict(
            database='mongo_dev',
            db_user='foo',
            db_pass='bar'
    ))
    client.secrets.kv.v2.create_or_update_secret(
        path='t-systems/cloud_billing/dev/application',
        secret=dict(
            client_id='dev000-001',
            environment='dev',
            log_level='debug'
    ))

    print('[INFO] Create kv example for test')
    client.secrets.kv.v2.create_or_update_secret(
        path='t-systems/cloud_billing/test/database',
        secret=dict(
            database='mongo_test',
            db_user='test_db',
            db_pass='password'
    ))
    client.secrets.kv.v2.create_or_update_secret(
        path='t-systems/cloud_billing/test/application',
        secret=dict(
            client_id='tst050-021',
            environment='test',
            log_level='debug'
    ))

    print('[INFO] Create kv example for prod')
    client.secrets.kv.v2.create_or_update_secret(
        path='t-systems/cloud_billing/prod/database',
        secret=dict(
            database='mongo_prod',
            db_user='super_secret_user',
            db_pass='secret_strong_password'
    ))
    client.secrets.kv.v2.create_or_update_secret(
        path='t-systems/cloud_billing/prod/application',
        secret=dict(
            client_id='prod723-346',
            environment='prod',
            log_level='warning'
    ))
    print('[INFO] Done')


def show_kv(client, kv_path):
    print('--------------------')
    print('[INFO] Show information about secret under path {path}'.format(
        path=kv_path
    ))
    secret_version_response = client.secrets.kv.v2.read_secret_version(
        path=kv_path
    )
    print('[INFO] Latest version contains the following keys: {data}'.format(
        data=secret_version_response['data']['data'].keys()
    ))
    print('[INFO] Latest version created at: {date}'.format(
        date=secret_version_response['data']['metadata']['created_time']
    ))
    print('[INFO] Latest version is #{ver}'.format(
        ver=secret_version_response['data']['metadata']['version']
    ))

    print('--------------------')
    print('[INFO] Show pair "key: value" for path {path}'.format(
        path=kv_path
    ))
    kv_data = client.kv.v2.read_secret_version(path=kv_path)['data']['data']
    for item in kv_data:
        print('{key}: {value}'.format(key=item, value=kv_data[item]))


def create_policy(client, env):
    policy_body = """
    path "secret/data/t-systems/cloud_billing/%s/*" {
        capabilities = ["create", "read", "update", "delete", "list"]}
    """ % env
    policy_name = "my-policy-" + env
    client.sys.create_or_update_policy(name=policy_name, policy=policy_body)


def create_read_policy(client):
    policy_body = """
    path "secret/data/*" {
        capabilities = ["read", "list"]}
    """
    client.sys.create_or_update_policy(name='my-policy-read', policy=policy_body)


def create_write_policy(client):
    policy_body = """
    path "secret/data/*" {
        capabilities = ["create", "read", "update", "delete", "list"]}
    """
    client.sys.create_or_update_policy(name='my-policy-write', policy=policy_body)


def create_secure_policy(client):
    policy_body = """
    path "secret/data/*" {
        capabilities = ["read", "list"]}

    path "secret/data/t-systems/cloud_billing/prod/*" {
        capabilities = ["deny"]}
    """
    client.sys.create_or_update_policy(name='my-policy-secure', policy=policy_body)


def show_policies(client):
    list_policies_resp = client.sys.list_policies()['data']['policies']
    print('List of currently configured policies: %s' % list_policies_resp)


def show_policy(client, policy_name):
    hvac_policy_rules = client.sys.read_policy(name=policy_name)['data']['rules']
    print('Rules for the {policy} policy are: {rules}'.format(
        policy=policy_name, rules=hvac_policy_rules
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

    create_kv(client)
    show_kv(client,'t-systems/cloud_billing/dev/application')

    create_policy(client, 'dev')
    create_policy(client, 'test')
    create_policy(client, 'prod')
    create_read_policy(client)
    create_write_policy(client)
    create_secure_policy(client)


if __name__ == '__main__':
    sys.exit(main())
