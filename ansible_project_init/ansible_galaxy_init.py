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
        return

    data = get_yaml_file_content(INSTALL_INFO_PATH_FORMAT % role)

    return data.get("version")


def install_dependencies(requirements_file):
    required_roles = get_yaml_file_content(requirements_file)

    for role in required_roles:
        src = role.get("src")
        name = role.get("name") if role.get("name") else src
        req_version = role.get("version")

        if not src:
            continue

        cur_version = get_installed_version(src)

        if is_version_installed(cur_version, req_version):
            print("%s (%s) is already installed." % (src, cur_version))
            continue

        install_dependency(src, cur_version, req_version, name)


def is_version_installed(cur_version, req_version):
    return cur_version and (not req_version or cur_version == req_version)


def get_yaml_file_content(file):
    f = open(file, "r")
    try:
        data = yaml.safe_load(f.read())
    except yaml.YAMLError as e:
        print("Unable to load data from the file {}: {}"
              .format(file, str(e)))
        data = {}
    finally:
        f.close()

    return data


def install_dependency(src, cur_version, req_version, name):
    command = [
        "ansible-galaxy",
        "install",
        "%s,%s,%s" % (src, req_version, name)
    ]

    if cur_version and cur_version != req_version:
        command.append("--force")

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
