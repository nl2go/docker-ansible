[![Travis (.org) branch](https://img.shields.io/travis/nl2go/docker-ansible/master)](https://travis-ci.org/nl2go/docker-ansible)
[![Codecov](https://img.shields.io/codecov/c/github/nl2go/docker-ansible)](https://codecov.io/gh/nl2go/docker-ansible)
[![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/nl2go/docker-ansible)](https://codeclimate.com/github/nl2go/docker-ansible)[
![Docker Pulls](https://img.shields.io/docker/pulls/nl2go/ansible)](https://hub.docker.com/r/nl2go/ansible)
[![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/nl2go/docker-ansible)](https://hub.docker.com/repository/docker/nl2go/ansible/tags?page=1)

# Docker Ansible

Containerized [Ansible](https://www.ansible.com/) CLI.

Contains additional tools/packages (s. [Dockerfile](Dockerfile)).

## Usage

Place the [docker-compose.yml](dist/docker-compose.yml) into your Ansible project and run 
    
    $ docker-compose run ansible

### SSH Agent

While using  SSH key authentication method to access remote resources, ensure that the encrypted private
key is located at the `.ssh/id_rsa` path within the user directory.

 - Linux/macOS: `$HOME/.ssh/id_rsa`
 - Windows: `$USERPROFILE/.ssh/id_rsa`

After starting the Ansible container the key passphrase will be prompted.

    $ docker-compose run ansible
    Starting SSH Agent.
    Enter passphrase for /root/.ssh/id_rsa: 

### Ansible Vault

[Ansible Vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html) allows to keep sensitive data like
passwords or keys encrypted. It supports encryption of whole files as well as single variables.

To clearly separate
and restrict access to different inventories/environments multiple Ansible Vault passwords are indispensable.

When operating Ansible playbooks frequently, typing the Vault password on every execution can be cumbersome, especially
with multiple environments in place.

While offering a possibility to reference password files, Ansible Vault does not provide a convenient feature to create or
manage those, apart from the fact that an official integration into a password manager like
[Gnome-Keyring](https://de.wikipedia.org/wiki/Gnome_Keyring) doesn't exist.

To overcome the limitations of the status quo a convenient method to manage multiple Ansible Vault password
files is provided.

#### Create Encrypted Password Files

Initially an encrypted password file for every inventory/environment must be created using a personal master and environment
related Ansible Vault password. This is a one time operation per inventory/environment. Add `.vault-password` to the
`gitignore` patterns to prevent accidental check-ins.

    $ cd inventories/prod
    $ ansible-encrypt-vault-password
    Enter the master password for .vault-password files:
    Enter the vault password for prod inventory:
    Created /ansible/inventories/prod/.vault-password.
   
   
As a result master password encrypted `inventories/prod/.vault-password` file that contains the environment Ansible Vault
password is created.

#### Load Encrypted Password Files

The encrypted password files are loaded when a new container is started.
 
    $ docker-compose run ansible
    ...
    Decrypting Ansible Vault passwords.
    Enter decryption password for .vault-password files: 
    Decrypting /ansible/inventories/prod/.vault-password.
    
    
Alternatively encrypted password files may be reloaded within existing container.

    $ cd /ansible
    $ ansible-vault-init
    Decrypting Ansible Vault passwords.
    Enter decryption password for .vault-password files: 
    Decrypting /ansible/inventories/prod/.vault-password.

#### Encrypt Secrets
Secret values are encrypted per inventory (e.g. inventory `prod`, secret value `foo`).

    $ ansible-vault encrypt_string --encrypt-vault-id 'prod' 'foo'
    !vault |
              $ANSIBLE_VAULT;1.2;AES256;production-de
              33636332626264316661363731393861333764313361326262313664336435366666306664636434
              3339643439333138303035373866363265326132653363380a303937343963303530666337396561
              31626334633162323731323539393330366633386338393439613332373362383137383930616362
              3066383536323139610a616434643664613435356365356330636435633666353864626439626335
              6664

### Ansible Galaxy

Bigger Ansible projects frequently utilize Ansible Galaxy Roles that can be installed using a `requirements.yml` file.
Roles installation can be triggered from the container.

    $ cd /ansible
    ansible-galaxy-init
    Skipping Ansible Galaxy roles installation. No "/ansible/roles/requirements.yml" file present.

It's a tiny wrapper for `ansible-galaxy install -r /ansible/roles/requirements.yml` that ensures that the `requirements.yml`
is placed into the right location expected by [Ansible Tower](https://www.ansible.com/products/tower).

## Development

You can run the locally build image with:

    docker-compose run ansible

To rebuild the image run:

    docker-compose build

## Maintainers

- [build-failure](https://github.com/build-failure)

## License

See the [LICENSE.md](LICENSE.md) file for details
