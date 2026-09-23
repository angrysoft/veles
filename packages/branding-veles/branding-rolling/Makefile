VERSION=rolling
VERSION_NO_DOT=`echo ${VERSION} | sed 's:\.::g'`
THEME=Veles

all: info veles.d

info:
	echo "Make sure to have rsvg-view, GraphicsMagick and optipng installed"

veles.d: grub2.d plymouth.d

veles.d_clean:

CLEAN_DEPS+=veles.d_clean


grub2.d:
	mkdir -p Veles/grub2
	cp -a boot/grub2/theme Veles/grub2/

grub2.d_clean:
	rm -rf Veles/grub2

CLEAN_DEPS+=grub2.d_clean

plymouth.d:
	mkdir -p Veles/plymouth
	cp plymouth/config/plymouthd.defaults Veles/plymouth

plymouth.d_clean:
	rm -rf Veles/plymouth

CLEAN_DEPS+=plymouth.d_clean

install:
	# Grub2 theme
	mkdir -p $(DESTDIR)/usr/share/grub2/themes/${THEME} ${DESTDIR}/boot/grub2/themes/${THEME}
	cp -a Veles/grub2/theme/* ${DESTDIR}/usr/share/grub2/themes/${THEME}
	perl -pi -e "s/THEME_NAME/${THEME}/" ${DESTDIR}/usr/share/grub2/themes/${THEME}/activate-theme
	# Plymouth default config (jsc#SLE-11637)
	mkdir -p $(DESTDIR)/usr/share/plymouth/
	cp Veles/plymouth/plymouthd.defaults $(DESTDIR)/usr/share/plymouth
	# Brand file
	mkdir -p $(DESTDIR)/etc
	cp Veles-brand $(DESTDIR)/etc/

clean: ${CLEAN_DEPS}
	rmdir Veles
