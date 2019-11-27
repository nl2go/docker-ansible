#!/usr/bin/python

from ansible_project_init import ssh_agent_init
from ansible_project_init import ansible_vault_init
from ansible_project_init import ansible_galaxy_init


def init():
    ssh_agent_init.init()
    ansible_vault_init.init()
    ansible_galaxy_init.init()
