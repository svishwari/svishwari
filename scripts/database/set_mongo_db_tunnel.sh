# This script is to setup an SSH tunnel to access databse
#!/bin/bash

BASTION_HOST="ops001.mgnt.us-east-1.mgnt-xspdev.in"
DOC_DB_USER=${1:-${USER}}

if [[ -z "$DOC_DB_USER" ]]; then
	read -p "Username: " DOC_DB_USER
fi

ssh $DOC_DB_USER@$BASTION_HOST -L $DATABASE_LOCAL_PORT:$DATABASE_HOST:$DATABASE_PORT
