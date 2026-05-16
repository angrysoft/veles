#!/bin/sh

# z katalogu veles/
sudo kiwi-ng --debug system build \
  --description . \
  --target-dir /tmp/veles-build |tee log.txt


