#
# spec file for package magicq
#

%define _pkgver 1_9_8_3

Name:           magicq
Version:        1.9.8.3
Release:        0
Summary:        Lighting control software from ChamSys
License:        custom
URL:            https://chamsyslighting.com/products/magicq
Source0:        magicq-installer.sh
Source1:        magicq-uninstaller.sh

BuildArch:      x86_64
BuildRequires:  tar
BuildRequires:  binutils
BuildRequires:  fdupes
Requires:       alsa
Requires:       libjack0
Requires:       gstreamer-plugins-base
Requires:       gstreamer-plugins-good
# Requires:       libarchive13
# Requires:       cups-libs
Requires:       Mesa-libGL1
# Requires:       libX11-6
# Requires:       libxcb1
Requires:       systemd-udev
# Requires:       zlib

%description
Lighting control software from ChamSys for professional stage and event production.

%prep
ar x %{SOURCE0}

%build
# 

%install
%{__mkdir_p} %{buildroot}/opt/magicq
%{__mkdir_p} %{buildroot}%{_bindir}
%{__mkdir_p} %{buildroot}%{_datadir}/licenses/%{name}

tar -xf data.tar.xz -C %{buildroot}

# Usuwamy biblioteki systemowe dostarczane z paczką na rzecz bibliotek z openSUSE:
# https://secure.chamsys.co.uk/help/documentation/magicq/troubleshooting.html#_linux_magicq_fails_to_start_libgl_error
rm -rf %{buildroot}/opt/magicq/lib/libstdc++.so.6
rm -rf %{buildroot}/opt/magicq/lib/libjack.so.0

# for dir in log show web thumbs backuparchive convert audio; do
#     %{__mkdir_p} %{buildroot}/opt/magicq/$dir
# done

ln -s /opt/magicq/License_Conditions.txt %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

ln -s /opt/magicq/runmagicq.sh %{buildroot}%{_bindir}/magicq
ln -s /opt/magicq/runmagichd.sh %{buildroot}%{_bindir}/magichd
ln -s /opt/magicq/runmagicvis.sh %{buildroot}%{_bindir}/magicvis

find %{buildroot}/usr %{buildroot}/etc -type f -exec chmod 644 {} + , -type d -exec chmod 755 {} +
%fdupes %{buildroot}%{_prefix}


%files
%{_bindir}/magicq
%{_bindir}/magichd
%{_bindir}/magicvis
%{_datadir}/licenses/%{name}
%{_datadir}/applications
%{_datadir}/mime/packages/magicq.xml
%{_datadir}/pixmaps
/etc/udev
/etc/udev/rules.d
/opt/magicq
