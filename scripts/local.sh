#!/usr/bin/env sh
docker run --rm \
  --name dreamscrape-local \
  -v `pwd`:/repo \
  --workdir /repo \
  --user `id -u`:`id -g` \
  -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
  -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
  -e AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} \
  -e GITHUB_USER=${GITHUB_USER} \
  -e GITHUB_PASSWORD=${GITHUB_PASSWORD} \
  --tty --interactive \
  dreamscrape:latest \
  /bin/bash
