FROM ubuntu:20.04

LABEL MAINTAINER=<ops@newsletter2go.com>

ARG ANSIBLE_VERSION=2.8.*

RUN apt-get update && apt-get -y install \
    sudo \
    wget \
    openssl \
    ca-certificates \
    openssh-client \
    python3 \
    python3-dev \
    python3-pip \
    libffi-dev \
    libssl-dev \
    build-essential \
  && pip3 install ansible==$ANSIBLE_VERSION

RUN wget -O /tmp/teleport.deb 'https://get.gravitational.com/teleport_4.2.10_amd64.deb' \
  && dpkg -i /tmp/teleport.deb && rm -f /tmp/teleport.deb

RUN ln -fsn /usr/bin/python3 /usr/bin/python
RUN ln -fsn /usr/bin/pip3 /usr/bin/pip

RUN pip install \
  ansible-filter==1.1.1 \
  netaddr==0.7.19 \
  pymongo

COPY .docker/ /
COPY ansible_project_init/ /opt/ansible_project_init/ansible_project_init
COPY setup.py /opt/ansible_project_init/setup.py
RUN pip install -e /opt/ansible_project_init

WORKDIR /ansible

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["/bin/bash"]
