#!/bin/bash
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='hvs.lKjpo7yohps676dm77XACGFQ'

newpass=$(openssl rand -base64 12)
vault kv put secret/app-config username="test-user" password="$newpass"

echo "Secret rotated at $(date) to $newpass"

