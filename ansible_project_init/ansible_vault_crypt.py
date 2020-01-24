#!/usr/bin/python

import os
import subprocess
import getpass


confirm_msg_template = \
    'File {} already exists. Do you want to replace it? (y/n): '
prompt_master_password_msg = \
    'Enter the master password for .vault-password files: '
prompt_vault_password_msg_template = \
    'Enter the vault password for {} inventory: '


def get_input(msg):
    return input(msg)


def encrypt_vault_password():
    base_dir = os.getcwd()
    encrypted_vault_password_file = base_dir + '/.vault-password'
    confirm_msg = confirm_msg_template.format(encrypted_vault_password_file)
    if is_file_exist(encrypted_vault_password_file) \
            and not is_confirm(confirm_msg):
        return

    inventory_name = os.path.basename(base_dir)
    master_password = prompt_password(prompt_master_password_msg)
    vault_password = prompt_password(
        prompt_vault_password_msg_template.format(inventory_name)
    )
    encrypt_content_to_file(
        vault_password,
        master_password,
        encrypted_vault_password_file
    )
    print('Created {}.'.format(encrypted_vault_password_file))


def prompt_password(prompt):
    return getpass.getpass(
        prompt=prompt,
        stream=None
    )


def is_confirm(msg):
    confirmation = get_input(msg)
    confirmation = confirmation.lower().strip()
    if confirmation == 'y':
        return True
    else:
        return False


def is_file_exist(file):
    return os.path.isfile(file)


def encrypt_content_to_file(content, password, encrypted_file):
    return call(
        'echo {}| openssl enc -aes-256-cbc -pbkdf2 -pass pass:{} > {}',
        content,
        password,
        encrypted_file
    )


def decrypt_file_to_file(password, encrypted_file, decrypted_file):
    return call(
        'openssl enc -d -aes-256-cbc -pbkdf2 -pass pass:{} < {} > {}',
        password,
        encrypted_file,
        decrypted_file
    )


def call(
    command_template,
    password,
    encrypted_file,
    decrypted_file
):
    command = command_template.format(
        password,
        encrypted_file,
        decrypted_file
    )
    return subprocess.call(command, shell=True)
