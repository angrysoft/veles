#
# spec file for package veles-base
#
# Copyright (c) 2026 Angrysoft Sebastian Zwierzchowski <sebastian.zwierzchowski@gmail.com>
#
# SPDX-License-Identifier: MIT
#

%define product Veles
%define codename Rolling

Name:           veles-base
Version:        0.1.0
Release:        1
Summary:        Veles Linux
License:        MIT
Group:          System/Fhs
BuildArch:      noarch
Provides:       distribution-base
Provides:       product-update() = dup

Requires: aaa_base
Requires: aaa_base-extras
Requires: apparmor-abstractions
Requires: apparmor-parser
Requires: apparmor-profiles
Requires: apparmor-utils
Requires: audit
Requires: bash
Requires: btrfsprogs
Requires: bzip2
Requires: ca-certificates-mozilla
Requires: chrony
Requires: coreutils
Requires: coreutils-systemd
Requires: curl
Requires: dosfstools
Requires: dracut
Requires: e2fsprogs
Requires: efibootmgr
Requires: elfutils
Requires: file
Requires: filesystem
Requires: findutils
Requires: fwupd
Requires: fwupd-lang
Requires: glibc
Requires: glibc-locale
Requires: glibc-locale-base
Requires: grep
Requires: grml-zsh-config
Requires: gzip
Requires: hostname
Requires: iproute2
Requires: kexec-tools
Requires: kernel-default
Requires: kernel-firmware-all
Requires: lastlog2
Requires: less
Requires: libblockdev
Requires: libnss_usrfiles2
Requires: man
Requires: ncurses-utils
Requires: neovim
Requires: NetworkManager
Requires: ntfs-3g
Requires: ntfsprogs
Requires: openssh
Requires: pam
Requires: pam-config
Requires: pam_pwquality
Requires: parted
Requires: pciutils
Requires: perl-base
Requires: procps
Requires: rpm
Requires: sed
Requires: shadow
Requires: smartmontools
Requires: sudo
Requires: system-group-wheel
Requires: system-user-bin
Requires: system-user-daemon
Requires: system-user-nobody
Requires: systemd
Requires: systemd-boot
Requires: systemd-lang
Requires: tar
Requires: terminfo
Requires: terminfo-base
Requires: terminfo-screen
Requires: time
Requires: timezone
Requires: tuned
Requires: udisks2
Requires: udisks2-lang
Requires: udisks2-zsh-completion
Requires: udev
Requires: unzip
Requires: usbutils
Requires: util-linux
Requires: util-linux-lang
Requires: util-linux-systemd
Requires: wget
Requires: which
Requires: wtmpdb
Requires: xz
Requires: zip
Requires: zsh

%description
Veles Linux — base configs

%prep

%build

%install
mkdir -p %{buildroot}%{_sysconfdir}/sudoers.d

cat > %{buildroot}%{_sysconfdir}/sudoers.d/wheel <<EOF
%wheel ALL=(ALL:ALL) NOPASSWD: ALL
EOF
chown root:root %{buildroot}%{_sysconfdir}/sudoers.d/wheel
chmod 0440 %{buildroot}%{_sysconfdir}/sudoers.d/wheel


%files
%dir %{_sysconfdir}/sudoers.d
%{_sysconfdir}/sudoers.d/wheel

%changelog
* Sat May 16 2026 AngrySoft <sebastian.zwierzchowski@gmail.com>
- Initial veles-release package