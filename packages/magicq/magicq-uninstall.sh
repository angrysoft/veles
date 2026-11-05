#!/bin/sh

rm -rf /opt/magicq/
rm -f /usr/local/bin/magicq
rm -f /usr/local/bin/magichd
rm -f /usr/local/bin/magicvis
rm -f /etc/udev/rules.d/99-chamsys-usb.rules
rm -f /usr/share/applications/magichd.desktop
rm -f /usr/share/applications/magicmultiwin.desktop
rm -f /usr/share/applications/magicq.desktop
rm -f /usr/share/applications/magicvis.desktop
rm -f /usr/share/mime/packages/magicq.xml
rm -f /usr/share/pixmaps/magichd.png
rm -f /usr/share/pixmaps/magicq.png
rm -f /usr/share/pixmaps/magicvis.png

if command -v update-mime-database >/dev/null 2>&1; then
    update-mime-database /usr/share/mime || true
fi
exit 0
