FROM ubuntu:16.04

LABEL MAINTAINER=<ops@newsletter2go.com>

ARG ANSIBLE_VERSION=2.7
ARG DEBIAN_FRONTEND=noninteractive

ENV ANSIBLE_CONFIG=/ansible/ansible.cfg
ENV ANSIBLE_ACTION_PLUGINS=/ansible/plugins/action_plugins

RUN echo "deb http://ppa.launchpad.net/ansible/ansible-$ANSIBLE_VERSION/ubuntu xenial main" | tee /etc/apt/sources.list.d/ansible.list \
    && echo "deb-src http://ppa.launchpad.net/ansible/ansible-$ANSIBLE_VERSION/ubuntu xenial main" | tee -a /etc/apt/sources.list.d/ansible.list \
    && apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 7BB9C367 \
    && apt-get update \
    && apt-get install -y \
               ansible \
               python-pip \
               python-pymongo \
               python-jmespath \
               nano \
               vim \
               less \
               curl \
               dnsutils \
               traceroute \
               mtr \
               telnet \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U pip
RUN pip install ansible_merge_vars

COPY .docker/ /
COPY ansible_project_init/ /opt/ansible_project_init

RUN ln -fsn /opt/ansible_project_init/main.py /usr/bin/ansible-project-init

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["/bin/bash"]
