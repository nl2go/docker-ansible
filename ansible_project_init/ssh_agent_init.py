#!/usr/bin/python

import os
import subprocess
import re
import shutil

from ansible_project_init import env_config


def create_ssh_dir_if_not_exists(ssh_dir):
    if not os.path.exists(ssh_dir):
        os.makedirs(ssh_dir, 0o700)


def copy_private_key(tmp_private_key, private_key):
    shutil.copyfile(tmp_private_key, private_key)
    os.chmod(private_key, 0o600)


def is_file_exist(file):
    return os.path.isfile(file)


def run_ssh_agent():
    output = subprocess.check_output('ssh-agent').decode()
    output_pattern = re.compile(
        'SSH_AUTH_SOCK=(?P<socket>[^;]+).*SSH_AGENT_PID=(?P<pid>\\d+)',
        re.MULTILINE | re.DOTALL
    )
    match = output_pattern.search(output)
    if match is None:
        raise Exception(''
                        'Could not parse ssh-agent output: {}'.format(output)
                        )

    agent_data = match.groupdict()
    set_ssh_agent_env_config(agent_data)
    env_config.write_ssh_agent_config(agent_data)


def set_ssh_agent_env_config(agent_data):
    os.environ['SSH_AUTH_SOCK'] = agent_data.get('socket')
    os.environ['SSH_AGENT_PID'] = agent_data.get('pid')


def add_ssh_key():
    subprocess.call('ssh-add')


def init():
    tmp_ssh_dir = '/tmp/.ssh'
    tmp_private_key = tmp_ssh_dir + '/id_rsa'
    ssh_dir = '/root/.ssh'
    private_key = ssh_dir + '/id_rsa'

    if is_file_exist(tmp_private_key):
        print('Starting SSH Agent.')
        create_ssh_dir_if_not_exists(ssh_dir)
        copy_private_key(tmp_private_key, private_key)
        run_ssh_agent()
        add_ssh_key()
    else:
        print(
            'Skipping SSH Agent start. No private key was found at {}.'
            .format(tmp_private_key)
        )
