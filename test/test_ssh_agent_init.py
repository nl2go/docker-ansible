import unittest

from unittest import mock
from ansible_project_init import ssh_agent_init


class SshAgentInitTest(unittest.TestCase):

    @mock.patch('subprocess.check_output')
    @mock.patch('os.makedirs')
    @mock.patch('os.chmod')
    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    @mock.patch('shutil.copyfile')
    @mock.patch('subprocess.call')
    def test_init(
        self,
        mock_call,
        mock_copyfile,
        mock_is_file,
        mock_path_exists,
        mock_chmod,
        mock_make_dirs,
        mock_check_output
    ):
        mock_copyfile.side_effect = self.verify_copy_private_key
        mock_is_file.return_value = True
        mock_path_exists.return_value = False
        mock_chmod.side_effect = self.verify_private_key_chmod
        mock_make_dirs.side_effect = self.verify_ssh_dir_chmod
        mock_check_output.return_value =\
            'SSH_AUTH_SOCK=/tmp/ssh-TIVv4l2O49GZ/agent.78;' \
            'export SSH_AUTH_SOCK;SSH_AGENT_PID=79;' \
            'export SSH_AGENT_PID; echo Agent pid 79;'.encode()
        mock_call.return_value = 0

        ssh_agent_init.init()

    @mock.patch('os.path.isfile')
    def test_init_skip(self, mock_is_file):
        mock_is_file.return_value = False

        ssh_agent_init.init()

    def verify_private_key_chmod(self, private_key, mode):
        self.assertEqual('/root/.ssh/id_rsa', private_key)
        self.assertEqual(0o600, mode)

    def verify_ssh_dir_chmod(self, ssh_dir, mode):
        self.assertEqual('/root/.ssh', ssh_dir)
        self.assertEqual(0o700, mode)

    def verify_copy_private_key(self, source, target):
        self.assertEqual('/tmp/.ssh/id_rsa', source)
        self.assertEqual('/root/.ssh/id_rsa', target)
