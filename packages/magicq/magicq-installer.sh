#!/bin/sh

set -e
TMPDIR=$(mktemp -d)
cd "$TMPDIR"
wget https://secure.chamsys.co.uk/downloads/v1_9_8_3/magicq_ubuntu_v1_9_8_3.deb
ar x magicq_ubuntu_v1_9_8_3.deb
mkdir /opt/magicq
tar -xvf data.tar.xz
rm -rf opt/magicq/lib/libstdc++.so.6
rm -rf opt/magicq/lib/libjack.so.0
cp -r opt/* /opt/magicq/
ln -s /opt/magicq/runmagicq.sh /usr/local/bin/magicq
ln -s /opt/magicq/runmagichd.sh /usr/local/bin/magichd
ln -s /opt/magicq/runmagicvis.sh /usr/local/bin/magicvis
install -m 644 etc/udev/rules.d/99-chamsys-usb.rules /etc/udev/rules.d/
install -m 644 usr/share/applications/magichd.desktop /usr/share/applications/
install -m 644 usr/share/applications/magicmultiwin.desktop /usr/share/applications/
install -m 644 usr/share/applications/magicq.desktop /usr/share/applications/
install -m 644 usr/share/applications/magicvis.desktop /usr/share/applications/
install -m 644 usr/share/mime/packages/magicq.xml /usr/share/mime/packages/
install -m 644 usr/share/pixmaps/magichd.png /usr/share/pixmaps/
install -m 644 usr/share/pixmaps/magicq.png /usr/share/pixmaps/
install -m 644 usr/share/pixmaps/magicvis.png /usr/share/pixmaps/

update-mime-database /usr/share/mime
