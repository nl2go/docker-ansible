#!/bin/ash

PYTHONPATH=/opt/ansible-project-init

python -m ansible_project_init && ash -c "$*"
