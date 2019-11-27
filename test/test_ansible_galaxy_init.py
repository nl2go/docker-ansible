import unittest
import os
import tempfile

from unittest import mock
from ansible_project_init import ansible_galaxy_init


class AnsibleGalaxyInitTest(unittest.TestCase):

    @mock.patch('subprocess.call')
    @mock.patch('os.getcwd')
    def test_init(self, mock_os_getcwd, mock_subprocess_call):
        base_dir = tempfile.TemporaryDirectory('r')
        role_dir = base_dir.name + '/roles'
        os.makedirs(role_dir, exist_ok=True)
        requirements_file = role_dir + '/requirements.yml'
        open(requirements_file, 'a').close()
        mock_os_getcwd.return_value = base_dir.name
        mock_subprocess_call.side_effect = (
            lambda command: self.assertEqual(
                command,
                ['ansible-galaxy', 'install', '-r', requirements_file]
            )
        )

        ansible_galaxy_init.init()

        base_dir.cleanup()

    @mock.patch('os.getcwd')
    def test_init_skip(self, mock_os_getcwd):
        base_dir = '/tmp'
        mock_os_getcwd.return_value = base_dir

        ansible_galaxy_init.init()
