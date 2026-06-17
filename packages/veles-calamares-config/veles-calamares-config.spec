#
# spec file for package veles-calamares-config
#
# Copyright (c) 2026 Angrysoft Sebastian Zwierzchowski <sebastian.zwierzchowski@gmail.com>
#
# SPDX-License-Identifier: MIT
#

Name:           veles-calamares-config
Version:        0.1.0
Release:        2
Summary:        Minimalistyczna konfiguracja i branding Calamares dla Veles Linux
License:        GPL-3.0-or-later
URL:            https://github.com/angrysoft/veles/packages/veles-calamares-config
Group:          System/Management

Requires:       calamares
Requires:       calamares-lang
Requires:       libqt5-qtwayland
Requires:       cantarell-fonts
Requires:       sway
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
Source3:        partition.conf
Source4:        users.conf
Source5:        branding.desc
Source6:        stylesheet.qss
Source7:        veles-logo.png
Source8:        welcome.png

BuildArch:      noarch

%description
Veles Linux — installer settings

%prep
# No tarball to unpack

%build
# No binaries to compile

%install
# Main configuration
install -Dm 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/calamares/settings.conf

# Modules configuration
install -Dm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/calamares/modules/unpackfs.conf
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/calamares/modules/bootloader.conf
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/calamares/modules/partition.conf
install -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/calamares/modules/users.conf

# Branding and styling
install -Dm 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/calamares/branding/veles/branding.desc
install -Dm 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/calamares/branding/veles/show.qml
install -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/calamares/branding/veles/stylesheet.qss
install -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/calamares/branding/veles/veles-logo.png
install -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/calamares/branding/veles/welcome.png


%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/calamares
%dir %{_sysconfdir}/calamares/branding
%dir %{_sysconfdir}/calamares/branding/veles
%dir %{_sysconfdir}/calamares/modules

%{_sysconfdir}/calamares/settings.conf
%{_sysconfdir}/calamares/modules/unpackfs.conf
%{_sysconfdir}/calamares/modules/bootloader.conf
%{_sysconfdir}/calamares/modules/partition.conf
%{_sysconfdir}/calamares/modules/users.conf
%{_sysconfdir}/calamares/branding/veles/branding.desc
%{_sysconfdir}/calamares/branding/veles/show.qml
%{_sysconfdir}/calamares/branding/veles/stylesheet.qss
%{_sysconfdir}/calamares/branding/veles/veles-logo.png
%{_sysconfdir}/calamares/branding/veles/welcome.png


%changelog
* Sat May 16 2026 AngrySoft <sebastian.zwierzchowski@gmail.com>
- Initial veles-release package