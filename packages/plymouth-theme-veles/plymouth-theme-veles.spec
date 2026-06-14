Name:           plymouth-theme-veles
Version:        0.1.0
Release:        1%{?dist}
Summary:        Plymouth boot splash theme for Veles Linux
License:        MIT
URL:            https://github.com/angrysoft/veles
BuildArch:      noarch

Source0:        veles.plymouth
Source1:        veles.script
Source2:        logo.png

BuildRequires:  dracut
BuildRequires:  plymouth
BuildRequires:  plymouth-plugin-script
%{?dracut_modules_prereq}

Requires:       plymouth
Requires:       plymouth-plugin-script

%description
Plymouth theme for Veles linux

%prep

%build

%install
install -d %{buildroot}%{_datadir}/plymouth/themes/veles/images

install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/plymouth/themes/veles/veles.plymouth
install -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/plymouth/themes/veles/veles.script
install -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/plymouth/themes/veles/images/logo.png


%post
if [ -d /run/systemd/system ] || [ ! -f /.buildenv ]; then
    if [ -x /usr/sbin/plymouth-set-default-theme ]; then
        /usr/sbin/plymouth-set-default-theme veles >/dev/null 2>&1 || true
    fi
    %{?regenerate_initrd_post}
fi

%postun
if [ $1 -eq 0 ]; then
    if [ -d /run/systemd/system ] || [ ! -f /.buildenv ]; then
        if [ -x /usr/sbin/plymouth-set-default-theme ]; then
            /usr/sbin/plymouth-set-default-theme text >/dev/null 2>&1 || true
        fi
        %{?regenerate_initrd_postun}
    fi
fi

%posttrans
if [ -d /run/systemd/system ] || [ ! -f /.buildenv ]; then
    %{?regenerate_initrd_posttrans}
fi

%files
%dir %{_datadir}/plymouth/themes/veles/
%dir %{_datadir}/plymouth/themes/veles/images/
%{_datadir}/plymouth/themes/veles/veles.plymouth
%{_datadir}/plymouth/themes/veles/veles.script
%{_datadir}/plymouth/themes/veles/images/logo.png

%changelog
* Sun Jun 14 2026 Sebastian Angrysoft <angrysoft@example.com> - 0.1.0-1
- Pierwsza wersja motywu Veles
