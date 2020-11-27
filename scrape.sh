#!/usr/bin/env bash

git config --global credential.helper '!f() { sleep 1; echo "username=${GIT_USER}"; echo "password=${GIT_PASSWORD}"; }; f'
cd /tmp


set -xe

git clone --depth=1 --no-single-branch https://github.com/bertbesser/DreamScrape.git



pushd DreamScrape

git checkout scrape-all

dvc pull

dvc repro

dvc add dreams
dvc push

git add .
git push

