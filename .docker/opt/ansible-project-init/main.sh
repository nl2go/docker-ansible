#!/bin/bash

source /opt/log-util/main.sh

WORKING_DIR="$(pwd)"
PROJECT_NAME="$(basename "$WORKING_DIR")"

if [ -z "$INVENTORIES_PATH" ]; then
  INVENTORIES_PATH="${WORKING_DIR}/inventories"
fi

function decryptInventoryPasswordFile(){
  local encryptedVaultPasswordFile="$1"
  local inventoryName
  local decryptedVaultPasswordFile

  inventoryName=$(basename "$(dirname "$decryptedVaultPasswordFile")")
  decryptedVaultPasswordFile="/tmp/.vault-password-${projectName}-${inventoryName}"
  openssl enc -d -aes-256-cbc -pass env:VAULT_PASSWORD_PASSWORD < "${encryptedVaultPasswordFile}" > "${decryptedVaultPasswordFile}"
  info -n "${projectName}-${inventoryName}@${decryptedVaultPasswordFile},"
}

function decryptInventoryPasswordFiles(){
  local projectName
  local inventoriesPath
  local identityList

  projectName="$1"
  inventoriesPath="$2"

  info "Load and decrypt inventory password files for project ${projectName}."
  if [ "$(find "${inventoriesPath}" -mindepth 2 -maxdepth 2 -name .vault-password | wc -l)" -gt 0 ]; then
    info -n Enter decryption password for .vault-password files
    read -s -r -p ": " VAULT_PASSWORD_PASSWORD ; echo
    export VAULT_PASSWORD_PASSWORD
    identityList=$(find "${inventoriesPath}" -mindepth 2 -maxdepth 2 -name .vault-password | \
      while read -r encryptedVaultPasswordFile; do
        info "Decrypt $encryptedVaultPasswordFile."
        decryptInventoryPasswordFile "$encryptedVaultPasswordFile"
      done)
    export VAULT_PASSWORD_PASSWORD=""
    export ANSIBLE_VAULT_IDENTITY_LIST=${identityList%,}
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
