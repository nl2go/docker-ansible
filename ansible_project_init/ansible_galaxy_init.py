#!/usr/bin/python

import os
import subprocess
import yaml

INSTALL_INFO_PATH_FORMAT = os.path.expanduser("~/.ansible/roles/%s/meta/.galaxy_install_info")


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
        print("Unable to load data from the requirements file: {}".format(str(e)))
        return None

    return install_info["version"]


def install_dependencies(requirements_file):
    f = open(requirements_file, "r")
    try:
        required_roles = yaml.safe_load(f.read())
    except yaml.YAMLError as e:
        print("Unable to load data from the requirements file: {}".format(str(e)))
        return

    for role in required_roles:
        required_src = role["src"] if "src" in role else None
        required_version = role["version"] if "version" in role else None

        if not required_src:
            continue

        installed_version = get_installed_version(required_src)

        if installed_version and (not required_version or installed_version == required_version):
            print("%s (%s) is already installed." % (required_src, installed_version))
            continue

        force = "--force" if installed_version and installed_version != required_version else ""

        command = ["ansible-galaxy", "install", "%s,%s" % (required_src, required_version), force]
        subprocess.call(command)


def init():
    base_dir = os.getcwd()
    requirements_file = base_dir + "/roles/requirements.yml"
    if is_file(requirements_file):
        print("Installing Ansible Galaxy roles from {}.".format(requirements_file))
        install_dependencies(requirements_file)
    else:
        print("Skipping Ansible Galaxy roles installation. No {} file present.".format(requirements_file))
