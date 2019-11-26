#!/usr/bin/python

import os
import subprocess


def is_file(file):
    return os.path.isfile(file)


def install_dependencies(requirements_file):
    command = 'ansible-galaxy install -r "{}"'.format(requirements_file)
    subprocess.call(command)


def init():
    base_dir = os.getcwd()
    requirements_file = base_dir + '/roles/requirements.yml'
    if is_file(requirements_file):
        print(
            'Installing Ansible Galaxy roles from "{}".'
            .format(requirements_file)
        )
        install_dependencies(requirements_file)
    else:
        print(
            'Skipping Ansible Galaxy roles installation. No "{}" file present.'
            .format(requirements_file)
        )
