#
# spec file for package veles-base
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
Requires:       cage
Requires:       polkit

Requires:       parted
Requires:       e2fsprogs
Requires:       dosfstools
Requires:       btrfsprogs
Requires:       systemd-boot
Requires:       calamares-lang

Source0:        settings.conf
Source1:        unpackfs.conf
Source2:        bootloader.conf
Source3:        partitions.conf
Source4:        users.conf
Source5:        branding.desc
Source6:        logo.png
Source7:        welcome.png
Source8:        stylesheet.qss

BuildArch:      noarch

%description
Veles Linux — installer settings

%prep

%build

%install
mkdir -p %{buildroot}%{_sysconfdir}/calamares/modules
mkdir -p %{buildroot}%{_sysconfdir}/calamares/branding/veles

install -m 644 settings.conf %{buildroot}%{_sysconfdir}/calamares/settings.conf


install -m 644 unpackfs.conf %{buildroot}%{_sysconfdir}/calamares/modules/unpackfs.conf
install -m 644 bootloader.conf %{buildroot}%{_sysconfdir}/calamares/modules/bootloader.conf
install -m 644 partitions.conf %{buildroot}%{_sysconfdir}/calamares/modules/partitions.conf
install -m 644 users.conf %{buildroot}%{_sysconfdir}/calamares/modules/users.conf

# Instalacja plików brandingu (opisy i grafiki)
install -m 644 branding.desc %{buildroot}%{_sysconfdir}/calamares/branding/veles/branding.desc
install -m 644 stylesheet.qss %{buildroot}%{_sysconfdir}/calamares/branding/veles/stylesheet.qss
install -m 644 logo.png %{buildroot}%{_sysconfdir}/calamares/branding/veles/logo.png
install -m 644 welcome.png %{buildroot}%{_sysconfdir}/calamares/branding/veles/welcome.png



%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/calamares/settings.conf
%config(noreplace) %{_sysconfdir}/calamares/modules/unpackfs.conf
%config(noreplace) %{_sysconfdir}/calamares/modules/bootloader.conf
%config(noreplace) %{_sysconfdir}/calamares/modules/partitions.conf
%config(noreplace) %{_sysconfdir}/calamares/modules/users.conf
%config(noreplace) %{_sysconfdir}/calamares/modules/stylesheet.qss


# Pliki brandingu
%{_sysconfdir}/calamares/branding/default/

%changelog
* Sat May 16 2026 AngrySoft <sebastian.zwierzchowski@gmail.com>
- Initial veles-release package