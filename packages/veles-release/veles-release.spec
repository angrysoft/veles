#
# spec file for package veles-release
#
# Copyright (c) 2026 Angrysoft Sebastian Zwierzchowski <sebastian.zwierzchowski@gmail.com>
#
# SPDX-License-Identifier: MIT
#

%define product Veles
%define codename Rolling

Name:           veles-release
Version:        0.1.0
Release:        1
Summary:        Veles Linux
License:        MIT
Group:          System/Fhs
BuildArch:      noarch
# Zastępujemy openSUSE-release
Provides:       distribution-release
Provides:       openSUSE-release = %{version}-%{release}
Provides:       suse-release = %{version}-%{release}
Obsoletes:      openSUSE-release < %{version}

# Wymagany flavor (tworzymy go poniżej)
Requires:       product_flavor(veles)

# Mechanizm zypper dup zamiast up
Provides:       product-update() = dup

# Identyfikacja produktu dla zypp
Provides:       product() = veles
Provides:       product(veles) = %{version}-%{release}
Provides:       product-label() = Veles

%ifarch x86_64
Provides:       product-register-target() = Veles-x86_64
%endif
%ifarch aarch64
Provides:       product-register-target() = Veles-aarch64
%endif

Conflicts:      distribution-release

%description
Veles Linux — a RPM-based rolling distribution.

%package -n veles-release-base
License:        MIT
Group:          System/Fhs
Summary:        Veles Linux base flavor
Provides:       product_flavor()
Provides:       flavor(base)
Provides:       product_flavor(veles) = %{version}-%{release}

%description -n veles-release-base
Base product flavor for Veles Linux.

%files -n veles-release-base
%defattr(-,root,root)
%doc %{_defaultdocdir}/veles-release-base

# ---- prep / build / install ----
%prep

%build

%install
# /etc i /usr/lib
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_prefix}/lib/motd.d
mkdir -p %{buildroot}%{_prefix}/lib/issue.d

# os-release
cat > %{buildroot}%{_prefix}/lib/os-release <<EOF
NAME="Veles Linux"
ID="veles"
ID_LIKE="opensuse suse"
VERSION="%{version}"
VERSION_ID="%{version}"
PRETTY_NAME="Veles Linux %{version}"
ANSI_COLOR="1;35"
HOME_URL="https://github.com/angrysoft/veles"
BUG_REPORT_URL="https://github.com/angrysoft/veles/issues"
EOF

ln -s ..%{_prefix}/lib/os-release %{buildroot}%{_sysconfdir}/os-release

# issue / motd
echo -e 'Veles Linux \\r (\\l)\n' \
    > %{buildroot}%{_prefix}/lib/issue.d/90-veles.issue
echo "Welcome to Veles Linux." \
    > %{buildroot}%{_prefix}/lib/motd.d/welcome

# products.d
mkdir -p %{buildroot}%{_sysconfdir}/products.d
cat > %{buildroot}%{_sysconfdir}/products.d/veles.prod <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<product schemeversion="0">
  <vendor>Veles</vendor>
  <name>veles</name>
  <version>%{version}</version>
  <release>%{release}</release>
  <arch>%{_target_cpu}</arch>
  <productline>Veles</productline>
  <summary>Veles Linux</summary>
  <shortsummary>Veles</shortsummary>
  <description>Veles Linux — a RPM-based rolling distribution.</description>
  <installconfig>
    <defaultlang>en_US</defaultlang>
    <releasepackage name="veles-release" flag="EQ" version="%{version}" release="%{release}"/>
    <distribution>veles</distribution>
  </installconfig>
  <runtimeconfig/>
</product>
EOF

# baseproduct symlink (wymagany przez zypp)
ln -s veles.prod %{buildroot}%{_sysconfdir}/products.d/baseproduct

# vendor config
mkdir -p %{buildroot}%{_sysconfdir}/zypp/vendors.d
cat > %{buildroot}%{_sysconfdir}/zypp/vendors.d/00-veles.conf <<EOF
[main]
vendors=Veles,obs://build.opensuse.org/home:angrysoft:veles,openSUSE,SUSE
EOF

# flavor doc
mkdir -p %{buildroot}%{_defaultdocdir}/veles-release-base
echo "Base flavor for Veles Linux." \
    > %{buildroot}%{_defaultdocdir}/veles-release-base/README

%files
%defattr(644,root,root,755)
%{_sysconfdir}/os-release
%{_prefix}/lib/os-release
%dir %{_prefix}/lib
%dir %{_prefix}/lib/issue.d
%dir %{_prefix}/lib/motd.d
%{_prefix}/lib/issue.d/90-veles.issue
%{_prefix}/lib/motd.d/welcome
%dir %{_sysconfdir}/products.d
%{_sysconfdir}/products.d/veles.prod
%{_sysconfdir}/products.d/baseproduct
%dir %{_sysconfdir}/zypp
%dir %{_sysconfdir}/zypp/vendors.d
%config %{_sysconfdir}/zypp/vendors.d/00-veles.conf

%changelog
* Sat May 16 2026 AngrySoft <sebastian.zwierzchowski@gmail.com>
- Initial veles-release package
