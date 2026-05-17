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

%description
Veles Linux — base configs

%prep

%build

%install
mkdir -p %{buildroot}%{_sysconfdir}/sudoers.d

cat > %{buildroot}%{_sysconfdir}/sudoers.d/wheel <<EOF
%wheel ALL=(ALL:ALL) NOPASSWD: ALL
EOF

%files
%dir %{_sysconfdir}/sudoers.d
%{_sysconfdir}/sudoers.d/wheel

%changelog
* Sat May 16 2026 AngrySoft <sebastian.zwierzchowski@gmail.com>
- Initial veles-release package