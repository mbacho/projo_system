#!/usr/bin/env bash

#Clean project folder to clear out unnecessary stuff

#remove folders
for i in build coverage_html_reports dbs eggs items logs project.egg-info; do
    if [ -e "$i" ]; then
        rm -rf "$i"
    fi
done

#remove files
for i in .coverage twistd.pid setup.py; do
    if [ -e "$i" ]; then
        rm "$i"
    fi
done

