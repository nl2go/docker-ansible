#!/bin/bash

source /opt/log-util/main.sh

info "Set up SSH agent with the supplied key."
mkdir -p /root/.ssh
cp /tmp/.ssh/* /root/.ssh/
chmod 600 /root/.ssh/*
eval $(ssh-agent) &>/dev/null \
    && ssh-add &>/dev/null \
    && bash -c "$*"
