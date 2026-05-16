#!/bin/sh

# z katalogu veles/
sudo rm -rf /tmp/veles-build
sudo kiwi-ng --debug system build \
  --description . \
  --target-dir /tmp/veles-build |tee log.txt


