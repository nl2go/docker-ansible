#!/bin/bash

PYTHONPATH=/opt/ansible-project-init

python -m ansible_project_init && bash -c "$*"
