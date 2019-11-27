#!/usr/bin/python

import glob
import os
import getpass

from ansible_project_init import ansible_vault_crypt
from ansible_project_init import env_config


def get_encrypted_vault_password_files(base_dir):
    return glob.glob(base_dir + '/inventories/**/.vault-password')


def prompt_encryption_password():
    return getpass.getpass(
        prompt='Enter decryption password for .vault-password files: ',
        stream=None
    )


def get_inventory_name(encrypted_vault_password_file):
    return os.path.basename(os.path.dirname(encrypted_vault_password_file))


def get_vault_password_file(inventory_name):
    return '/tmp/.vault-password-' + inventory_name


def get_vault_id(inventory_name, vault_password_file):
    return '{}@{}'.format(inventory_name, vault_password_file)


def decrypt_vault_password_files(encrypted_vault_password_files):
    vault_ids = []
    encryption_password = prompt_encryption_password()
    for encrypted_vault_password_file in encrypted_vault_password_files:
        print('Decrypting {}.'.format(encrypted_vault_password_file))
        inventory_name = get_inventory_name(encrypted_vault_password_file)
        vault_password_file = get_vault_password_file(inventory_name)
        vault_id = get_vault_id(inventory_name, vault_password_file)
        ansible_vault_crypt.decrypt_file_to_file(
            encryption_password,
            encrypted_vault_password_file,
            vault_password_file
        )
        vault_ids.append(vault_id)
    return vault_ids


def init():
    base_dir = os.getcwd()
    encrypted_vault_password_files = get_encrypted_vault_password_files(
        base_dir
    )
    if encrypted_vault_password_files:
        print('Decrypting Ansible Vault passwords.')
        vault_ids = decrypt_vault_password_files(encrypted_vault_password_files)
        env_config.write_ansible_vault_config(vault_ids)
    else:
        print(
            'Skpping Anisble Vault password decryption. '
            'No .vault-password files present.'
        )
