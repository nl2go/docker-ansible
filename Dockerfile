FROM alpine:3.10.3

LABEL MAINTAINER=<ops@newsletter2go.com>

ARG ANSIBLE_VERSION=2.7

RUN apk --update --no-cache add \
    sudo \
    openssl \
    ca-certificates \
    openssh-client \
    python3 \
  && apk --no-cache --virtual build-dependencies add \
    python3-dev \
    libffi-dev \
    openssl-dev \
    build-base \
  && pip3 install ansible==$ANSIBLE_VERSION \
  && apk del build-dependencies

RUN ln -fsn /usr/bin/python3 /usr/bin/python
RUN ln -fsn /usr/bin/pip3 /usr/bin/pip

COPY .docker/ /
COPY ansible_project_init/ /opt/ansible_project_init

RUN ln -fsn /opt/ansible_project_init/ansible_vault_crypt.py /usr/bin/ansible-vault-encrypt-password \
  && ln -fsn /opt/ansible_project_init/ansible_vault_init.py /usr/bin/ansible-vault-init \
  && ln -fsn /opt/ansible_project_init/ansible_galaxy_init.py /usr/bin/ansible-galaxy-init \
  && ln -fsn /opt/ansible_project_init/ssh_agent_init.py /usr/bin/ssh-agent-init

WORKDIR /ansible

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["/bin/ash"]
