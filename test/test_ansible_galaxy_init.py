import unittest
import os
import tempfile
from io import StringIO

from unittest import mock
from ansible_project_init import ansible_galaxy_init
from ansible_project_init.ansible_galaxy_init import INSTALL_INFO_PATH_FORMAT


def create_file(file_path, lines):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w+", encoding="utf-8") as f:
        for line in lines:
            f.write(line)
        f.close()


class AnsibleGalaxyInitTest(unittest.TestCase):
    @mock.patch("subprocess.call")
    @mock.patch("os.getcwd")
    def test_init(self, mock_os_getcwd, mock_subprocess_call):
        expected_package = "some.package"
        expected_version = "1991"

        base_dir = tempfile.TemporaryDirectory("r")
        requirement_lines = [
            "- src: %s\n" % expected_package,
            "  version: %s\n" % expected_version,
        ]
        requirements_file = "%s/roles/requirements.yml" % base_dir.name
        create_file(requirements_file, requirement_lines)

        mock_os_getcwd.return_value = base_dir.name
        mock_subprocess_call.side_effect = (
            lambda command: self.assertEqual(
                [
                    "ansible-galaxy",
                    "install",
                    "%s,%s,%s" % (
                        expected_package,
                        expected_version,
                        expected_package
                    )
                ],
                command
            )
        )

        ansible_galaxy_init.init()

        base_dir.cleanup()

    @mock.patch("subprocess.call")
    @mock.patch("os.getcwd")
    def test_init_with_alias(self, mock_os_getcwd, mock_subprocess_call):
        expected_package = "some.package.name"
        expected_version = "1991"
        expected_alias = "some.package.alias"

        base_dir = tempfile.TemporaryDirectory("r")
        requirement_lines = [
            "- src: %s\n" % expected_package,
            "  version: %s\n" % expected_version,
            "  name: %s\n" % expected_alias,
        ]
        requirements_file = "%s/roles/requirements.yml" % base_dir.name
        create_file(requirements_file, requirement_lines)

        mock_os_getcwd.return_value = base_dir.name
        mock_subprocess_call.side_effect = (
            lambda command: self.assertEqual(
                [
                    "ansible-galaxy",
                    "install",
                    "%s,%s,%s" % (
                        expected_package,
                        expected_version,
                        expected_alias
                    )
                ],
                command
            )
        )

        ansible_galaxy_init.init()

        base_dir.cleanup()

    @mock.patch("subprocess.call")
    @mock.patch("os.getcwd")
    def test_init_with_different_installed_version(
        self, mock_os_getcwd, mock_subprocess_call
    ):
        expected_package = "some.package"
        expected_version = "1991"
        installed_version = "1903"
        install_date = "28.05.1991"

        base_dir = tempfile.TemporaryDirectory("r")
        requirement_lines = [
            "- src: %s\n" % expected_package,
            "  version: %s\n" % expected_version,
        ]
        requirements_file = "%s/roles/requirements.yml" % base_dir.name
        create_file(requirements_file, requirement_lines)

        install_info_lines = [
            "install_date: %s\n" % install_date,
            "version: %s" % installed_version,
        ]
        installed_info_file = INSTALL_INFO_PATH_FORMAT % expected_package
        create_file(installed_info_file, install_info_lines)

        mock_os_getcwd.return_value = base_dir.name
        mock_subprocess_call.side_effect = (
            lambda command: self.assertEqual(
                [
                    "ansible-galaxy",
                    "install",
                    "%s,%s,%s" % (
                        expected_package,
                        expected_version,
                        expected_package
                    ),
                    "--force"
                ],
                command
            )
        )

        ansible_galaxy_init.init()

        base_dir.cleanup()

    @mock.patch("os.getcwd")
    def test_init_with_same_installed_version(self, mock_os_getcwd):
        expected_package = "some.package"
        expected_version = "1991"
        installed_version = expected_version
        install_date = "28.05.1991"

        base_dir = tempfile.TemporaryDirectory("r")
        requirement_lines = [
            "- src: %s\n" % expected_package,
            "  version: %s\n" % expected_version,
        ]
        requirements_file = "%s/roles/requirements.yml" % base_dir.name
        create_file(requirements_file, requirement_lines)

        install_info_lines = [
            "install_date: %s\n" % install_date,
            "version: %s" % installed_version,
        ]
        installed_info_file = INSTALL_INFO_PATH_FORMAT % expected_package
        create_file(installed_info_file, install_info_lines)

        mock_os_getcwd.return_value = base_dir.name

        ansible_galaxy_init.init()

        base_dir.cleanup()

    @mock.patch("os.getcwd")
    def test_init_without_src(self, mock_os_getcwd):
        base_dir = tempfile.TemporaryDirectory("r")
        requirement_lines = [
            "-  version: some.version",
        ]
        requirements_file = "%s/roles/requirements.yml" % base_dir.name
        create_file(requirements_file, requirement_lines)

        mock_os_getcwd.return_value = base_dir.name
        ansible_galaxy_init.init()

        base_dir.cleanup()

    @mock.patch("os.getcwd")
    def test_init_with_invalid_requirements_yaml(self, mock_os_getcwd):
        base_dir = tempfile.TemporaryDirectory("r")
        requirements_file = "%s/roles/requirements.yml" % base_dir.name
        expected_output = \
            "Unable to load data from the file %s" % requirements_file

        requirement_lines = [
            "some: invalid: yaml",
        ]

        create_file(requirements_file, requirement_lines)

        mock_os_getcwd.return_value = base_dir.name

        with mock.patch('sys.stdout', new=StringIO()) as fake_out:
            ansible_galaxy_init.init()
            self.assertIn(expected_output, fake_out.getvalue())

        base_dir.cleanup()

    @mock.patch("subprocess.call")
    @mock.patch("os.getcwd")
    def test_init_with_invalid_install_info_yaml(
        self, mock_os_getcwd, mock_subprocess_call
    ):
        expected_package = "some.package"
        installed_info_file = INSTALL_INFO_PATH_FORMAT % expected_package
        expected_version = "1991"
        expected_output = \
            "Unable to load data from the file %s" % installed_info_file

        requirement_lines = [
            "- src: %s\n" % expected_package,
            "  version: %s\n" % expected_version,
        ]

        base_dir = tempfile.TemporaryDirectory("r")
        requirements_file = "%s/roles/requirements.yml" % base_dir.name
        create_file(requirements_file, requirement_lines)

        install_info_lines = [
            "some: invalid: yaml",
        ]

        create_file(installed_info_file, install_info_lines)

        mock_os_getcwd.return_value = base_dir.name
        mock_subprocess_call.side_effect = (
            lambda command: self.assertEqual(
                [
                    "ansible-galaxy",
                    "install",
                    "%s,%s,%s" % (
                        expected_package,
                        expected_version,
                        expected_package
                    )
                ],
                command
            )
        )

        with mock.patch('sys.stdout', new=StringIO()) as fake_out:
            ansible_galaxy_init.init()
            self.assertIn(expected_output, fake_out.getvalue())

        base_dir.cleanup()

    @mock.patch("os.getcwd")
    def test_init_skip(self, mock_os_getcwd):
        base_dir = "/tmp"
        mock_os_getcwd.return_value = base_dir

        ansible_galaxy_init.init()

    @mock.patch("os.path.isfile")
    def test_is_not_installed(self, mock_is_file):
        mock_is_file.return_value = False

        self.assertIsNone(ansible_galaxy_init.get_installed_version('role'))
