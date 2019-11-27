#!/bin/ash

set -e

ansible-project-init

if test -f /tmp/.ansible-ssh-agent; then
    . /tmp/.ansible-ssh-agent
fi

ash -c "$*"
