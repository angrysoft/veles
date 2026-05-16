#!/bin/sh

# z katalogu veles/
sudo --debug kiwi-ng system build \
  --description . \
  --target-dir /tmp/veles-build |tee log.txt


