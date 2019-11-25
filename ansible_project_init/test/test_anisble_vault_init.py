import unittest
import tempfile

from ansible_project_init import ansible_vault_init


class AnsibleVaultInitTest(unittest.TestCase):

    def test_get_vault_id(self):
        self.assertEqual('foo@bar', ansible_vault_init.get_vault_id('foo', 'bar'))

    def test_encrypt_vault_password(self):
        vault_password = 'foo'
        encryption_password = 'bar'
        vault_password_file = tempfile.NamedTemporaryFile('r')
        encrypted_vault_password_file = tempfile.NamedTemporaryFile('r')
        ansible_vault_init.encrypt_vault_password_file(
          vault_password,
          encryption_password,
          encrypted_vault_password_file.name
        )

        ansible_vault_init.decrypt_vault_password_file(
          encryption_password,
          encrypted_vault_password_file.name,
          vault_password_file.name
        )

        actual_vault_password = vault_password_file.read()
        self.assertEqual(vault_password, actual_vault_password.rstrip())
        encrypted_vault_password_file.close()
        vault_password_file.close()
