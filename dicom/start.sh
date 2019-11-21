#!/bin/bash

until psql -c '\q'; do
  >&2
  echo "Postgres is unavailable or $PGDATABASE database does not exist"
  echo -e "\t Check: docker ps -a | grep postgres"
  echo "Sleeping for 10 seconds"
  sleep 10
done


# Set VERBOSE environment variable in docker-compose.yml to "--verbose", "--trace",
# or remove to set logging level for Orthanc process
Orthanc /etc/orthanc/ $VERBOSE
