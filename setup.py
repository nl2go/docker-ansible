from setuptools import setup

setup(
    name='ansible_project_init',
    version='1.0.0',
    entry_points={
        'console_scripts': [
            'ansible-project-init = ansible_project_init.__main__:init',
            'ansible-vault-init = '
            'ansible_project_init.ansible_vault_init:init',
            'ansible-galaxy-init = '
            'ansible_project_init.ansible_galaxy_init:init',
            'ssh-agent-init = ansible_project_init.ssh_agent_init:init',
            'ansible-encrypt-vault-password = '
            'ansible_project_init.ansible_vault_crypt:encrypt_vault_password'
        ],
    }
)
