

from framework.vault.setup.vault_setup import Vault

class VaultHelper:
    @staticmethod
    def get_secret(secret_path, secret_key):
        if not Vault.client or not Vault.isConnected:
            raise Exception("Vault connection is not established")
        
        try:
            # Retrieve the secret from Vault using the provided secret_path and secret_key
            response = Vault.client.secrets.kv.v2.read_secret_version(path=secret_path)
            if 'data' in response and secret_key in response['data'].get('data', {}):
                return response['data']['data'][secret_key]
            else:
                raise Exception("Error retrieving secret from Vault")
        except Exception as err:
            print("Error retrieving secret from Vault:", err)
            raise Exception("Error retrieving secret from Vault")
