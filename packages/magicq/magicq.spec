#
# spec file for package magicq
#


Name:           magicq
Version:        1.9.8.3
Release:        22
Summary:        Lighting control software from ChamSys
License:        custom
URL:            https://chamsyslighting.com/products/magicq
Source0:        magicq-installer.sh
Source1:        magicq-uninstall.sh

ExclusiveArch:  x86_64
BuildRequires:   curl
Requires:       tar
Requires:       binutils
Requires:       curl
Requires:       shared-mime-info
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
install -d %{buildroot}%{_bindir}
install -m 755 %{SOURCE0} %{buildroot}%{_bindir}/magicq-installer.sh
install -m 755 %{SOURCE1} %{buildroot}%{_bindir}/magicq-uninstall.sh

%post
/usr/bin/magicq-installer.sh || echo "magicq download/install failed; rerun /usr/bin/magicq-installer.sh" >&2

%postun
/usr/bin/magicq-uninstall.sh || :

%files
%{_bindir}/magicq-installer.sh              
%{_bindir}/magicq-uninstall.sh
