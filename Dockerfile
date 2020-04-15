FROM alpine:3.10.3

LABEL MAINTAINER=<ops@newsletter2go.com>

ARG ANSIBLE_VERSION=2.7.*

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

RUN pip install \
  ansible-filter==1.2.0 \
  netaddr==0.7.19

COPY .docker/ /
COPY ansible_project_init/ /opt/ansible_project_init/ansible_project_init
COPY setup.py /opt/ansible_project_init/setup.py
RUN pip install -e /opt/ansible_project_init

WORKDIR /ansible

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["/bin/ash"]
