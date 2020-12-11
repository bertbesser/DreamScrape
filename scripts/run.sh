#!/usr/bin/env sh
docker run --rm \
  --name dreamscrape-run \
  --user user \
  -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
  -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
  -e AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} \
  -e GIT_USER=${GITHUB_USER} \
  -e GIT_PASSWORD=${GITHUB_TOKEN} \
  --tty --interactive \
  dreamscrape:latest

