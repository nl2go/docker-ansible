[![Travis (.org) branch](https://img.shields.io/travis/nl2go/docker-ansible/master)](https://travis-ci.org/nl2go/docker-ansible)
[![Codecov](https://img.shields.io/codecov/c/github/nl2go/docker-ansible)](https://codecov.io/gh/nl2go/docker-ansible)
[![Docker Pulls](https://img.shields.io/docker/pulls/nl2go/ansible)](https://hub.docker.com/r/nl2go/ansible)
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

After starting the Anisble container the personal password to encrypt Ansible Vault password files will be prompted.

    $ docker-compose run ansible
    Starting SSH Agent.
    Enter passphrase for /root/.ssh/id_rsa: 
    Identity added: /root/.ssh/id_rsa (/root/.ssh/id_rsa)
    Skpping Anisble Vault password decryption. No .vault-password files were found!


## Development

You can run the locally build image with:

    docker-compose run ansible

To rebuild the image run:

    docker-compose build

## Maintainers

- [build-failure](https://github.com/build-failure)

## License

See the [LICENSE.md](LICENSE.md) file for details
