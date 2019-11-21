#!/bin/bash

source /opt/log-util/main.sh

WORKING_DIR="$(pwd)"
PROJECT_NAME="$(basename "$WORKING_DIR")"

if [ -z "$INVENTORIES_PATH" ]; then
  INVENTORIES_PATH="${WORKING_DIR}/inventories"
fi

function decryptInventoryPasswordFiles(){
  if [ $(find "${INVENTORIES_PATH}" -mindepth 2 -maxdepth 2 -name .vault-password | wc -l) -gt 0 ]; then
    info "Enter decryption password for .vault-password files:"
    read -s -r -p ": " VAULT_PASSWORD_PASSWORD ; echo
    export VAULT_PASSWORD_PASSWORD
    ANSIBLE_VAULT_IDENTITY_LIST=$(find "${INVENTORIES_PATH}" -mindepth 2 -maxdepth 2 -name .vault-password | \
      while read V; do
        INVENTORY_NAME=$(basename $(dirname $V))
        VAULT_PASSWORD_FILE="/tmp/.vault-password-${PROJECT_NAME}-${INVENTORY_NAME}"
        cat "${V}" | openssl enc -d -aes-256-cbc -pass env:VAULT_PASSWORD_PASSWORD > "${VAULT_PASSWORD_FILE}"
        echo -n "${PROJECT_NAME}-${INVENTORY_NAME}@${VAULT_PASSWORD_FILE},"
      done)
    export VAULT_PASSWORD_PASSWORD=""
    # remove trailing comma
    export ANSIBLE_VAULT_IDENTITY_LIST=${ANSIBLE_VAULT_IDENTITY_LIST%,}
  fi
}

function installProjectRoleDependencies(){
  local requirementsPath
  requirementsPath="$(pwd)/roles/requirements.yml"

  info "Install project role dependencies from ${requirementsPath} using Anisble Galaxy."
  ansible-galaxy install -r "$requirementsPath"
}

decryptInventoryPasswordFiles "$PROJECT_NAME" "$INVENTORIES_PATH"
installProjectRoleDependencies
