#!/usr/bin/env bash

psql -U postgres -c "CREATE USER $USER PASSWORD '$PASSWORD'"
psql -U postgres -c "CREATE DATABASE $DB_NAME OWNER $USER"
psql -U postgres -c "ALTER USER $USER CREATEDB"
