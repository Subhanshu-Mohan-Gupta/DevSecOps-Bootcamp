#!/bin/bash
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='hvs.lKjpo7yohps676dm77XACGFQ'

username=$(vault kv get -field=username secret/app-config)
password=$(vault kv get -field=password secret/app-config)

echo "App is using:"
echo "Username: $username"
echo "Password: $password"

