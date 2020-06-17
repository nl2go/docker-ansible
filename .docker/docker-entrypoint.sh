#!/bin/bash

set -e

ansible-project-init

if test -f /tmp/.ansible-project-init-env; then
    . /tmp/.ansible-project-init-env
fi

bash -c "$*"
