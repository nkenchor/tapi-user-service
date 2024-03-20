from framework.vault.setup.vault_setup import Vault
from framework.logger.utils.helper.logger_helper import log_event  # Ensure this path matches where log_event is defined

class VaultHelper:
    @staticmethod
    def get_secret(secret_path, secret_key):
        if not Vault.client or not Vault.isConnected:
            log_event("ERROR", "Vault connection is not established")
            raise Exception("Vault connection is not established")
        
        try:
            # Retrieve the secret from Vault using the provided secret_path and secret_key
            response = Vault.client.secrets.kv.v2.read_secret_version(path=secret_path)
            if 'data' in response and secret_key in response['data'].get('data', {}):
                secret_value = response['data']['data'][secret_key]
                log_event("INFO", f"Secret '{secret_key}' retrieved from Vault successfully.")
                return secret_value
            else:
                log_event("ERROR", "Error retrieving secret from Vault: Secret not found.")
                raise Exception("Error retrieving secret from Vault")
        except Exception as err:
            log_event("ERROR", f"Error retrieving secret from Vault: {err}")
            raise Exception("Error retrieving secret from Vault")
