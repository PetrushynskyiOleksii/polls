#!/usr/bin/env bash
# Wait for postgres

count=1
until [ $count -eq 5 ]
  do
     sleep 3
     python src/manage.py migrate && break
     count=$((count + 1))
  done

 if [ $count -lt 5 ]; then
  python src/manage.py runserver 0.0.0.0:8000
 fi
