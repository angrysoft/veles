%{?dracut_modules_prereq}

Name:           plymouth-theme-veles
Version:        0.1.0
Release:        1%{?dist}
Summary:        Plymouth boot splash theme for Veles Linux
License:        MIT
URL:            https://github.com/angrysoft/veles
BuildArch:      noarch

Source0:        %{name}-%{version}.tar.gz

Requires:       plymouth
Requires:       plymouth-plugin-script
BuildRequires:  findutils

%description
Motyw splash screenu Plymouth dla Veles Linux.
Ciemne tło (#19120c) z animowanym spinnerem i paskiem postępu
w kolorze bursztynowym (#fab473).

%prep
%autosetup

%build

%install
install -d %{buildroot}%{_datadir}/plymouth/themes/veles/images

install -m 0644 veles.plymouth \
    %{buildroot}%{_datadir}/plymouth/themes/veles/veles.plymouth

install -m 0644 veles.script \
    %{buildroot}%{_datadir}/plymouth/themes/veles/veles.script

install -m 0644 images/logo.png \
    %{buildroot}%{_datadir}/plymouth/themes/veles/images/logo.png

%post
if [ $1 -eq 1 ] || [ $1 -eq 2 ]; then
    plymouth-set-default-theme veles 2>/dev/null || true
fi

%postun
if [ $1 -eq 0 ]; then
    plymouth-set-default-theme text 2>/dev/null || true
fi

%post
if [ -x /usr/sbin/plymouth-set-default-theme ]; then
    /usr/sbin/plymouth-set-default-theme veles || true
fi
%%{?regenerate_initrd_post}

%postun
if [ $1 -eq 0 ]; then
    if [ -x /usr/sbin/plymouth-set-default-theme ]; then
        /usr/sbin/plymouth-set-default-theme script || true
    fi
fi
%%{?regenerate_initrd_postun}

%posttrans
# Faktyczne uruchomienie przebudowania na samym końcu transakcji RPM
%%{?regenerate_initrd_posttrans}

%files
%license LICENSE
%dir %{_datadir}/plymouth/themes/veles/
%dir %{_datadir}/plymouth/themes/veles/images/
%{_datadir}/plymouth/themes/veles/veles.plymouth
%{_datadir}/plymouth/themes/veles/veles.script
%{_datadir}/plymouth/themes/veles/images/logo.png

%changelog
* nie cze 14 2026 Sebastian Angrysoft <angrysoft@example.com> - 0.1.0-1
- Pierwsza wersja motywu Veles
