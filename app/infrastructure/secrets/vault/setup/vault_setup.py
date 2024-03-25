import hvac

from app.infrastructure.system.logger.utils.helper.logger_helper import log_event
from app.infrastructure.system.configuration.configuration import Config

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
                    log_event("INFO", "Connected successfully to Vault")
                else:
                    log_event("ERROR", "Authentication to Vault failed")
                    raise Exception("Authentication to Vault failed")
            except Exception as err:
                log_event("ERROR", f"Could not connect to Vault: {err}")
                raise err
        return Vault.client

    @staticmethod
    def disconnect():
        if Vault.client and Vault.isConnected:
            Vault.client = None
            Vault.isConnected = False
            log_event("INFO", "Disconnected from Vault")
