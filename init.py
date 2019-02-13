import hvac
import sys
import argparse


VAULT_URL='http://127.0.0.1:8200'


#Create key-value example: 2 keys for 2 environments
def create_kv(client):
    print('[INFO] Create kv example for dev environment')
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

    print('[INFO] Create kv example for prod environment')
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


#Create policy for full access to specific environment
def create_policy(client, env):
    policy_body = """
    path "secret/data/t-systems/cloud_billing/%s/*" {
        capabilities = ["create", "read", "update", "delete", "list"]}
    """ % env
    policy_name = "my-policy-" + env
    client.sys.create_or_update_policy(name=policy_name, policy=policy_body)
    print('[INFO] Create policy for {value} environment'.format(value=env))


#Create read-only policy
def create_read_policy(client):
    policy_body = """
    path "secret/data/*" {
        capabilities = ["read", "list"]}
    """
    client.sys.create_or_update_policy(name='my-policy-read', policy=policy_body)
    print('[INFO] Create read policy')


#Create read-restricted policy
def create_secure_policy(client):
    policy_body = """
    path "secret/data/*" {
        capabilities = ["read", "list"]}

    path "secret/data/t-systems/cloud_billing/prod/*" {
        capabilities = ["deny"]}
    """
    client.sys.create_or_update_policy(name='my-policy-secure', policy=policy_body)
    print('[INFO] Create secure policy')


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
    create_policy(client, 'dev')
    create_policy(client, 'prod')
    create_read_policy(client)
    create_secure_policy(client)


if __name__ == '__main__':
    sys.exit(main())
