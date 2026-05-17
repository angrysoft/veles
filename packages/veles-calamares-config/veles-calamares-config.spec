#
# spec file for package veles-calamares-config
#
# Copyright (c) 2026 Angrysoft Sebastian Zwierzchowski <sebastian.zwierzchowski@gmail.com>
#
# SPDX-License-Identifier: MIT
#

Name:           veles-calamares-config
Version:        0.1.0
Release:        1
Summary:        Minimalistyczna konfiguracja i branding Calamares dla Veles Linux
License:        GPL-3.0-or-later
URL:            https://github.com/angrysoft/veles/packages/veles-calamares-config
Group:          System/Management

Requires:       calamares
Requires:       calamares-lang
Requires:       weston
Requires:       polkit

Requires:       parted
Requires:       gparted
Requires:       e2fsprogs
Requires:       dosfstools
Requires:       btrfsprogs
Requires:       systemd-boot

Source0:        settings.conf
Source1:        unpackfs.conf
Source2:        bootloader.conf
Source3:        partitions.conf
Source4:        users.conf
Source5:        branding.desc
Source6:        stylesheet.qss
Source7:        calamares-installer.service
Source8:        weston.ini
Source9:        veles-logo.png
Source10:      welcome.png

BuildArch:      noarch

%description
Veles Linux — installer settings

%prep
# No tarball to unpack

%build
# No binaries to compile

%install
install -Dm 644 settings.conf %{buildroot}%{_sysconfdir}/calamares/settings.conf

install -Dm 644 unpackfs.conf %{buildroot}%{_sysconfdir}/calamares/modules/unpackfs.conf
install -m 644 bootloader.conf %{buildroot}%{_sysconfdir}/calamares/modules/bootloader.conf
install -m 644 partitions.conf %{buildroot}%{_sysconfdir}/calamares/modules/partitions.conf
install -m 644 users.conf %{buildroot}%{_sysconfdir}/calamares/modules/users.conf

install -Dm 644 branding.desc %{buildroot}%{_sysconfdir}/calamares/branding/veles/branding.desc
install -m 644 stylesheet.qss %{buildroot}%{_sysconfdir}/calamares/branding/veles/stylesheet.qss
install -m 644 veles-logo.png %{buildroot}%{_sysconfdir}/calamares/branding/veles/veles-logo.png
install -m 644 welcome.png %{buildroot}%{_sysconfdir}/calamares/branding/veles/welcome.png

install -Dm 644 calamares-installer.service %{buildroot}%{_libdir}/systemd/system/calamares-installer.service
install -Dm 644 weston.ini %{buildroot}%{_sysconfdir}/xdg/weston/weston.ini



%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/calamares
%dir %{_sysconfdir}/calamares/branding
%dir %{_sysconfdir}/calamares/branding/veles
%dir %{_sysconfdir}/calamares/modules
%dir %{_sysconfdir}/xdg
%dir %{_sysconfdir}/xdg/weston
%dir %{_libdir}/systemd
%dir %{_libdir}/systemd/system

%{_sysconfdir}/calamares/settings.conf
%{_sysconfdir}/calamares/modules/unpackfs.conf
%{_sysconfdir}/calamares/modules/bootloader.conf
%{_sysconfdir}/calamares/modules/partitions.conf
%{_sysconfdir}/calamares/modules/users.conf
%{_sysconfdir}/calamares/branding/veles/branding.desc
%{_sysconfdir}/calamares/branding/veles/stylesheet.qss
%{_sysconfdir}/calamares/branding/veles/veles-logo.png
%{_sysconfdir}/calamares/branding/veles/welcome.png
%{_libdir}/systemd/system/calamares-installer.service
%{_sysconfdir}/xdg/weston/weston.ini

%changelog
* Sat May 16 2026 AngrySoft <sebastian.zwierzchowski@gmail.com>
- Initial veles-release package