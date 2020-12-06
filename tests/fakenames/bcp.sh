#!/bin/bash

echo "Create fake names database"
docker exec -i sybase isql \
-U sa -P myPassword -S MYSYBASE -D master \
-i /var/lib/dataset/fakenames.sql

echo "Import fake names using bcp"
docker exec -i sybase \
bcp master.dbo.fakenames in /var/lib/dataset/10k_fakenames_fra.txt \
-U sa -P myPassword -S MYSYBASE \
-c -J utf8 -Y -t '|' -r '\r\n' -m 999999999
