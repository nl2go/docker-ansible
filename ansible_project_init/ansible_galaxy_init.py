#!/usr/bin/python

import os
import subprocess
import yaml

INSTALL_INFO_PATH_FORMAT = os.path.expanduser(
    "~/.ansible/roles/%s/meta/.galaxy_install_info"
)


def is_file(file):
    return os.path.isfile(file)


def is_installed(role):
    return os.path.isfile(INSTALL_INFO_PATH_FORMAT % role)


def get_installed_version(role):
    if not is_installed(role):
        return None

    f = open(INSTALL_INFO_PATH_FORMAT % role, "r")
    try:
        install_info = yaml.safe_load(f.read())
    except yaml.YAMLError as e:
        print("Unable to load data from the requirements file: {}"
              .format(str(e)))
        return None

    return install_info["version"]


def install_dependencies(requirements_file):
    try:
        f = open(requirements_file, "r")
        required_roles = yaml.safe_load(f.read())
        f.close()
    except yaml.YAMLError as e:
        print("Unable to load data from the requirements file: {}"
              .format(str(e)))
        return

    for role in required_roles:
        required_src = role["src"] if "src" in role else None
        req_version = role["version"] if "version" in role else None

        if not required_src:
            continue

        cur_version = get_installed_version(required_src)

        if cur_version and \
            (not req_version or cur_version == req_version):

            print("%s (%s) is already installed." % (required_src, cur_version))
            continue

        force = "--force" if cur_version and cur_version != req_version else ""

        command = [
            "ansible-galaxy",
            "install",
            "%s,%s" % (required_src, req_version),
            force
        ]
        subprocess.call(command)


def init():
    base_dir = os.getcwd()
    requirements_file = base_dir + "/roles/requirements.yml"
    if is_file(requirements_file):
        print("Installing Ansible Galaxy roles from {}."
              .format(requirements_file))
        install_dependencies(requirements_file)
    else:
        print("Skipping Ansible Galaxy roles installation. No {} file present."
              .format(requirements_file))
