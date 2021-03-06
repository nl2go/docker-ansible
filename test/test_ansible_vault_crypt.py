import unittest
import tempfile

from unittest import mock
from ansible_project_init import ansible_vault_crypt


class AnsibleVaultCryptTest(unittest.TestCase):

    @mock.patch('os.getcwd')
    @mock.patch('getpass.getpass')
    def test_encrypt_vault_password(self, mock_getpass, mock_getcwd):
        password = 'bar'
        cwd = tempfile.TemporaryDirectory('r')
        mock_getpass.return_value = password
        mock_getcwd.return_value = cwd.name

        ansible_vault_crypt.encrypt_vault_password()

        self.assertTrue(ansible_vault_crypt.is_file_exist(
            cwd.name + '/.vault-password')
        )
        cwd.cleanup()

    @mock.patch('builtins.input')
    @mock.patch('os.path.isfile')
    @mock.patch('os.getcwd')
    @mock.patch('getpass.getpass')
    def test_encrypt_vault_password_with_confirm_n(
        self, mock_getpass, mock_getcwd, mock_is_file, mock_input
    ):
        password = 'bar'
        cwd = tempfile.TemporaryDirectory('r')
        mock_getpass.return_value = password
        mock_getcwd.return_value = cwd.name
        mock_is_file.return_value = True
        mock_input.return_value = 'n'

        self.assertFalse(ansible_vault_crypt.encrypt_vault_password())
        cwd.cleanup()

    def test_encrypt_decrypt_content(self):
        content = 'foo'
        password = 'bar'
        file = tempfile.NamedTemporaryFile('r')
        encrypted_file = tempfile.NamedTemporaryFile('r')
        ansible_vault_crypt.encrypt_content_to_file(
            content,
            password,
            encrypted_file.name
        )

        ansible_vault_crypt.decrypt_file_to_file(
            password,
            encrypted_file.name,
            file.name
        )

        actual_content = file.read().rstrip()
        encrypted_file.close()
        file.close()
        self.assertEqual(
            content,
            actual_content
        )

    @mock.patch('getpass.getpass')
    def test_prompt_password(self, mock_get_pass):
        password = 'foo'
        mock_get_pass.return_value = password

        actual_password = \
            ansible_vault_crypt.prompt_password('Bar:')

        self.assertEqual(
            password,
            actual_password
        )

    @mock.patch('ansible_project_init.ansible_vault_crypt.get_input')
    def test_is_confirm(self, mock_get_input):
        message = 'foo'
        mock_get_input.return_value = 'y'

        is_confirm = ansible_vault_crypt.is_confirm(message)

        self.assertTrue(is_confirm)

    @mock.patch('ansible_project_init.ansible_vault_crypt.get_input')
    def test_is_confirm_with_n(self, mock_get_input):
        message = 'foo'
        mock_get_input.return_value = 'n'

        is_confirm = ansible_vault_crypt.is_confirm(message)

        self.assertFalse(is_confirm)

    @mock.patch('builtins.input')
    def test_get_input(self, mock_input):
        expected = 'y'
        message = 'foo'
        mock_input.return_value = 'y'

        actual = ansible_vault_crypt.get_input(message)

        self.assertEqual(expected, actual)
