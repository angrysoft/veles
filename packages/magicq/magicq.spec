#
# spec file for package magicq
#

%define _pkgver 1_9_8_3

Name:           magicq
Version:        1.9.8.3
Release:        14
Summary:        Lighting control software from ChamSys
License:        custom
URL:            https://chamsyslighting.com/products/magicq
Source0:        magicq-installer.sh
Source1:        magicq-uninstaller.sh

ExclusiveArch:  x86_64
BuildRequires:  tar
BuildRequires:  binutils
Requires:       alsa
Requires:       libjack0
Requires:       gstreamer-plugins-base
Requires:       gstreamer-plugins-good
# Requires:       libarchive13
# Requires:       cups-libs
Requires:       Mesa-libGL1
Requires:       libX11
Requires:       libxcb
Requires:       systemd-udev
Requires:       zlib

%description
Lighting control software from ChamSys for professional stage and event production.

%prep

%build
# 

%install
install -D -m 755 %{SOURCE0} %{buildroot}%{_bindir}/magicq-installer.sh
install -D -m 755 %{SOURCE1} %{buildroot}%{_bindir}/magicq-uninstaller.sh

%post -p %{_bindir}/magicq-installer.sh

%postun -p %{_bindir}/magicq-uninstaller.sh

%files
%{_bindir}/magicq-installer.sh
%{_bindir}/magicq-uninstaller.sh
