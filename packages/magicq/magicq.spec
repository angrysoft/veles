#
# spec file for package magicq
#

%define _pkgver 1_9_8_3

Name:           magicq
Version:        1.9.8.3
Release:        1%{?dist}
Summary:        Lighting control software from ChamSys
License:        custom
URL:            https://chamsyslighting.com/products/magicq
Source0:        magicq_ubuntu_v%{_pkgver}.deb

BuildArch:      x86_64
BuildRequires:  tar
BuildRequires:  bintutils
Requires:       alsa
Requires:       libjack0
Requires:       gstreamer-plugins-base
Requires:       gstreamer-plugins-good
Requires:       libarchive13
Requires:       cups-libs
Requires:       Mesa-libGL1
Requires:       libX11-6
Requires:       libxcb1
Requires:       systemd-udev
Requires:       zlib

# Wyłączamy automatyczne sprawdzanie i generowanie zależności dla plików binarnych w /opt/magicq,
# ponieważ dostarczone tam biblioteki i binaria są prekompilowane przez producenta.
AutoReq:        no

%description
Lighting control software from ChamSys for professional stage and event production.

%prep
ar x %{SOURCE0}

%build
# Binaria są już skompilowane i zstripowane przez dostawcę.

%install
# Tworzymy strukturę katalogów w buildroot
%{__mkdir_p} %{buildroot}/opt/magicq
%{__mkdir_p} %{buildroot}%{_bindir}
%{__mkdir_p} %{buildroot}%{_datadir}/licenses/%{name}

# Rozpakowanie paczki .deb (archiver ar zawierający data.tar.xz)
tar -xf data.tar.xz -C %{buildroot}

# Usuwamy biblioteki systemowe dostarczane z paczką na rzecz bibliotek z openSUSE:
# https://secure.chamsys.co.uk/help/documentation/magicq/troubleshooting.html#_linux_magicq_fails_to_start_libgl_error
rm -rf %{buildroot}/opt/magicq/lib/libstdc++.so.6
rm -rf %{buildroot}/opt/magicq/lib/libjack.so.0

# Tworzenie katalogów roboczych i zapisywalnych wymaganych przez MagicQ
for dir in log show web thumbs backuparchive convert audio; do
    %{__mkdir_p} %{buildroot}/opt/magicq/$dir
done

# Podpięcie licencji
ln -s /opt/magicq/License_Conditions.txt %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

# Symlinki do /usr/bin
ln -s /opt/magicq/runmagicq.sh %{buildroot}%{_bindir}/magicq
ln -s /opt/magicq/runmagichd.sh %{buildroot}%{_bindir}/magichd
ln -s /opt/magicq/runmagicvis.sh %{buildroot}%{_bindir}/magicvis

# Poprawienie uprawnień dla plików i katalogów skopiowanych z .deb
find %{buildroot}/usr -type f -exec chmod 644 {} +
find %{buildroot}/usr -type d -exec chmod 755 {} +

%files
%defattr(-,root,root,-)
%{_bindir}/magicq
%{_bindir}/magichd
%{_bindir}/magicvis
%{_datadir}/licenses/%{name}

# Katalog /opt/magicq oraz jego zawartość wymagają uprawnień zapisu dla aplikacji
%attr(777,root,root) /opt/magicq
%attr(777,root,root) /opt/magicq/log
%attr(777,root,root) /opt/magicq/show
%attr(777,root,root) /opt/magicq/web
%attr(777,root,root) /opt/magicq/thumbs
%attr(777,root,root) /opt/magicq/backuparchive
%attr(777,root,root) /opt/magicq/convert
%attr(777,root,root) /opt/magicq/audio

# Pozostałe pliki z /opt/magicq (binaria, zasoby itp.)
/opt/magicq/*