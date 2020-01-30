import unittest
import tempfile
import os

from unittest import mock
from ansible_project_init import ansible_vault_init
from ansible_project_init import ansible_vault_crypt


class AnsibleVaultInitTest(unittest.TestCase):

    def test_get_vault_id(self):
        self.assertEqual(
            'foo@bar',
            ansible_vault_init.get_vault_id('foo', 'bar')
        )

    def test_get_vault_password_file(self):
        self.assertEqual(
            '/tmp/.vault-password-foo',
            ansible_vault_init.get_vault_password_file('foo')
        )

    def test_get_encrypted_vault_password_files(self):
        base_dir = tempfile.TemporaryDirectory('r')
        inventory_dir = base_dir.name + '/inventories/foo'
        os.makedirs(inventory_dir, exist_ok=True)
        open(inventory_dir + '/.vault-password', 'a').close()

        actual_encrypted_vault_password_files = ansible_vault_init \
            .get_encrypted_vault_password_files(base_dir.name)

        self.assertEqual(
            [base_dir.name + '/inventories/foo/.vault-password'],
            actual_encrypted_vault_password_files
        )
        base_dir.cleanup()

    @mock.patch('subprocess.call')
    @mock.patch('getpass.getpass')
    @mock.patch('os.getcwd')
    def test_init(self, mock_os_getcwd, mock_get_pass, mock_call):
        vault_password = 'foo'
        encryption_password = 'bar'
        mock_get_pass.return_value = encryption_password
        base_dir = tempfile.TemporaryDirectory('r')
        inventory_dir = base_dir.name + '/inventories/foo'
        os.makedirs(inventory_dir, exist_ok=True)
        encrypted_vault_password_file = inventory_dir + '/.vault-password'
        ansible_vault_crypt.encrypt_content_to_file(
            vault_password,
            encryption_password,
            encrypted_vault_password_file
        )
        mock_os_getcwd.return_value = base_dir.name
        mock_call.return_value = 0

        ansible_vault_init.init()

        base_dir.cleanup()

    @mock.patch('os.getcwd')
    def test_init_skip(self, mock_os_getcwd):
        mock_os_getcwd.return_value = '/tmp'

        ansible_vault_init.init()

    def test_decrypt_vault_password_files_after_5th(self):
        with self.assertRaises(SystemExit):
            ansible_vault_init.decrypt_vault_password_files([], 6)
