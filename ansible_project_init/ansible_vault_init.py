#!/usr/bin/python

import glob
import os
import getpass
import subprocess


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


def encrypt_vault_password_file(
    vault_password,
    encryption_password,
    encrypted_vault_password_file
):
    command = 'echo {} | openssl enc -aes-256-cbc -pass "pass:{}" > {}'.format(
          vault_password,
          encryption_password,
          encrypted_vault_password_file
    )
    subprocess.call(command, shell=True)


def decrypt_vault_password_file(
    encryption_password,
    encrypted_vault_password_file,
    vault_password_file
):
    command = 'openssl enc -d -aes-256-cbc -pass pass:{} < {} > {}'.format(
      encryption_password,
      encrypted_vault_password_file,
      vault_password_file
    )
    subprocess.call(command, shell=True)


def decrypt_vault_password_files(encrypted_vault_password_files):
    vault_ids = []
    encryption_password = prompt_encryption_password()
    for encrypted_vault_password_file in encrypted_vault_password_files:
        print('Processing {}.'.format(encrypted_vault_password_file))
        inventory_name = get_inventory_name(encrypted_vault_password_file)
        vault_password_file = get_vault_password_file(inventory_name)
        vault_id = get_vault_id(inventory_name, vault_password_file)
        decrypt_vault_password_file(
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
        decrypt_vault_password_files(encrypted_vault_password_files)
    else:
        print(
            'Skpping Anisble Vault password decryption. '
            'No .vault-password files were found!'
        )
