#!/usr/bin/env bash

psql -U postgres -c "CREATE USER $USER PASSWORD '$PASSWORD'"
psql -U postgres -c "CREATE DATABASE $DBNAME OWNER $USER"
