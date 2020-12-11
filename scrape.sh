#!/usr/bin/env bash

set -xe

git config --global credential.helper '!f() { sleep 1; echo "username=${GIT_USER}"; echo "password=${GIT_PASSWORD}"; }; f'

git clone --depth=1 --no-single-branch https://github.com/bertbesser/DreamScrape.git /tmp/DreamScrape
pushd /tmp/DreamScrape

git checkout scrape-all

dvc pull
dvc repro
dvc push

git add .
git push

