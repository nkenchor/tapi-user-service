import hvac
from configuration.configuration import Config

class Vault:
    client = None
    isConnected = False

    @staticmethod
    def connect():
        if not Vault.client or not Vault.isConnected:
            try:
                # Create a connection to Vault using the provided configuration
                Vault.client = hvac.Client(url=Config.Vault_url, token=Config.Vault_token)
                # Check if the connection is successful
                if Vault.client.is_authenticated():
                    Vault.isConnected = True
                    print("Connected successfully to Vault")
                else:
                    raise Exception("Authentication to Vault failed")
            except Exception as err:
                print("Could not connect to Vault:", err)
                raise err
        return Vault.client

    @staticmethod
    def disconnect():
        if Vault.client and Vault.isConnected:
            Vault.client = None
            Vault.isConnected = False
            print("Disconnected from Vault")
