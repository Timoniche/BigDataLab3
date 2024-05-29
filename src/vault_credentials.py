import configparser
import os
import pathlib

from ansible_vault import Vault


class WrongSecretNameException(Exception):
    pass


class VaultCredentials:
    def __init__(self):
        vault_pwd = os.getenv('VAULT_CREDS_PSW')
        self.vault = Vault(vault_pwd)

        cur_dir = pathlib.Path(__file__).parent.absolute()
        root_dir = cur_dir.parent

        config = configparser.ConfigParser()
        config.read(root_dir / 'config.ini')

        self.vault_env_path = root_dir / config['vault']['path']

        with open(self.vault_env_path) as vault_file:
            self.secrets = self.vault.load(vault_file.read())

    def get_secret(self, secret_name):
        try:
            return self.secrets[secret_name]
        except KeyError:
            raise WrongSecretNameException(f"There is no secret name: {secret_name}")
