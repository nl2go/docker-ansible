import sys
import unittest
import tempfile
import os
from unittest import mock

sys.modules['getpass'] = mock.MagicMock()
import getpass

from ansible_project_init import ansible_vault_init


class AnsibleVaultInitTest(unittest.TestCase):

    def test_get_vault_id(self):
        self.assertEqual('foo@bar', ansible_vault_init.get_vault_id('foo', 'bar'))

    def test_encrypt_vault_password(self):
        expected_vault_password = 'foo'
        encryption_password = 'bar'
        vault_password_file = tempfile.NamedTemporaryFile('r')
        encrypted_vault_password_file = tempfile.NamedTemporaryFile('r')
        ansible_vault_init.encrypt_vault_password_file(
          expected_vault_password,
          encryption_password,
          encrypted_vault_password_file.name
        )

        ansible_vault_init.decrypt_vault_password_file(
          encryption_password,
          encrypted_vault_password_file.name,
          vault_password_file.name
        )

        actual_vault_password = vault_password_file.read()
        self.assertEqual(expected_vault_password, actual_vault_password.rstrip())
        encrypted_vault_password_file.close()
        vault_password_file.close()

    def test_get_vault_password_file(self):
        self.assertEqual('/tmp/.vault-password-foo', ansible_vault_init.get_vault_password_file('foo'))

    def test_prompt_encryption_password(self):
        expected_encryption_password = 'foo'
        getpass.getpass.return_value = expected_encryption_password

        actual_encryption_password = ansible_vault_init.prompt_encryption_password()

        self.assertEqual(expected_encryption_password, actual_encryption_password)

    def test_get_encrypted_vault_password_files(self):
        base_dir = tempfile.TemporaryDirectory('r')
        inventory_dir = base_dir.name + '/inventories/foo'
        os.makedirs(inventory_dir, exist_ok=True)
        open(inventory_dir + '/.vault-password', 'a').close()

        actual_encrypted_vault_password_files = ansible_vault_init.get_encrypted_vault_password_files(base_dir.name)

        self.assertEqual([base_dir.name + '/inventories/foo/.vault-password'], actual_encrypted_vault_password_files)
        base_dir.cleanup()


