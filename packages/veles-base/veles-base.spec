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

# Base system
Requires:   aaa_base
Requires:   aaa_base-extras
Requires:   bash
Requires:   bzip2
Requires:   coreutils
Requires:   coreutils-systemd
Requires:   file
Requires:   filesystem
Requires:   findutils
Requires:   glibc
Requires:   glibc-locale
Requires:   glibc-locale-base
Requires:   grep
Requires:   gzip
Requires:   hostname
Requires:   less
Requires:   man
Requires:   ncurses-utils
Requires:   perl-base
Requires:   rpm
Requires:   sed
Requires:   tar
Requires:   terminfo
Requires:   terminfo-base
Requires:   terminfo-screen
Requires:   time
Requires:   timezone
Requires:   unzip
Requires:   util-linux
Requires:   util-linux-lang
Requires:   util-linux-systemd
Requires:   which
Requires:   xz
Requires:   zip

# Boot, kernel and firmware
Requires:   dracut
Requires:   efibootmgr
Requires:   fwupd
Requires:   fwupd-lang
Requires:   kexec-tools
Requires:   kernel-default
Requires:   kernel-firmware-all
Requires:   plymouth
Requires:   plymouth-theme-veles
Requires:   systemd-boot

# Filesystem and storage
Requires:   btrfsprogs
Requires:   btrfsmaintenance
Requires:   dosfstools
Requires:   e2fsprogs
Requires:   fstrim
Requires:   libblockdev
Requires:   ntfs-3g
Requires:   ntfsprogs
Requires:   parted
Requires:   smartmontools
Requires:   udev
Requires:   udisks2
Requires:   udisks2-lang
Requires:   udisks2-zsh-completion
Requires:   lastlog2
Requires:   lsof
Requires:   strace
Requires:   wtmpdb
Requires:   eza

# Security, auth and policy
Requires:   apparmor-abstractions
Requires:   apparmor-parser
Requires:   apparmor-profiles
Requires:   apparmor-utils
Requires:   audit
Requires:   pam
Requires:   pam-config
Requires:   pam_pwquality
Requires:   polkit
Requires:   polkit-default-privs
Requires:   run0-policy-wheel-auth-self
Requires:   run0-wrappers
Requires:   shadow
Requires:   system-group-wheel
Requires:   system-user-bin
Requires:   system-user-daemon
Requires:   system-user-nobody

# Networking and services
Requires:   bind-utils
Requires:   ca-certificates-mozilla
Requires:   chrony
Requires:   curl
Requires:   iproute2
Requires:   iputils
Requires:   NetworkManager
Requires:   openssh
Requires:   pciutils
Requires:   systemd
Requires:   systemd-lang
Requires:   tuned
Requires:   usbutils
Requires:   wget

# Shell, editor and user tools
Requires:   luajit-lpeg
Requires:   neovim
Requires:   ripgrep
Requires:   zsh
Requires:   zsh-syntax-highlighting
Requires:   veles-zsh-config


# Monitoring and system tools
Requires:   elfutils
Requires:   libnss_usrfiles2
Requires:   procps
Requires:   psmisc
Requires:   psmisc-lang

Source0:    polkit.run0-wheel.rules

%description
Veles Linux — base configs

%prep

%build

%install
install -Dm 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/polkit-1/rules.d/run0-wheel.rules

%files
%attr(0755, root,root) %dir %{_sysconfdir}/polkit-1
%attr(0755, root,root) %dir %{_sysconfdir}/polkit-1/rules.d
%attr(0644, root,root) %{_sysconfdir}/polkit-1/rules.d/run0-wheel.rules

%changelog
* Sat May 16 2026 AngrySoft <sebastian.zwierzchowski@gmail.com>
- Initial veles-release package