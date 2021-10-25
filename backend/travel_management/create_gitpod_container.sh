#!/bin/bash
if [ "$(ls | grep is_gitpod)" ];
then
    echo "Running in gitpod -> please wait for postgreSQL started" && sleep 30
else
    sleep 0
fi