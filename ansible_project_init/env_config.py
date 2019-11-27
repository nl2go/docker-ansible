#!/usr/bin/python

env_config_file = '/tmp/.ansible-project-init-env'


def write_ssh_agent_config(agent_data):
    file = open(env_config_file, "a+")
    write_ln(file, 'export SSH_AUTH_SOCK=' + agent_data.get('socket'))
    write_ln(file, 'export SSH_AGENT_PID=' + agent_data.get('pid') + '')
    file.close()


def write_ansible_vault_config(vault_ids):
    file = open(env_config_file, "a+")
    write_ln(file, 'export ANSIBLE_VAULT_IDENTITY_LIST=' + ','.join(vault_ids))
    file.close()


def write_ln(file, value):
    file.write(value + '\n')
