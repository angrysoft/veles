#
# spec file for package branding-veles
#


%define theme_name Veles
%define theme_version rolling
%define theme_version_clean Rolling
%define date 20260923

%ifarch x86_64 %{ix86}
%define gfxboot 1
%endif

%ifarch %{arm} aarch64 %{ix86} x86_64 riscv64 ppc64le
%define grub2 1
%endif

Name:           branding-%{theme_name}
Version:        1.0.0.%{date}
Release:        0
Summary:        %{theme_name} %{theme_version_clean} Brand File
License:        BSD-3-Clause AND CC-BY-SA-3.0 AND GPL-2.0-or-later
URL:            https://github.com/openSUSE/branding
Source0:        branding-%{theme_version}.zip
BuildRequires:  GraphicsMagick
# BuildRequires:  distribution-logos-openSUSE-Tumbleweed
BuildRequires:  fdupes
BuildRequires:  fribidi
BuildRequires:  optipng
%if 0%{?suse_version} >= 1550
# rsvg-convert used to be packaged together with rsvg-view in one package. With the removal
# of the rsvg-view program, this package was renamed to rsvg-convert (which is more fitting)
BuildRequires:  rsvg-convert
%else
BuildRequires:  rsvg-view
%endif
BuildRequires:  suse-module-tools
BuildRequires:  unzip
Conflicts:      branding-openSUSE
Provides:       branding
%if 0%{?suse_version} > 1320
BuildRequires:  update-bootloader-rpm-macros
%endif
# # These complete the distribution wallpaper selection
# # Taken from last Leap release starting by 16.0
# %if 0%{?suse_version} >= 1600
# Suggests:       wallpapers-openSUSE-extra
# %endif

%description
This package contains the file %{_sysconfdir}/veles-brand, and its name is used as
a trigger for installation of correct vendor brand packages.


%if 0%{?grub2} > 0
%package -n grub2-branding-%{theme_name}
Summary:        %{theme_name} %{theme_version_clean} branding for GRUB2
License:        CC-BY-SA-3.0
Requires:       (grub2 or grub2-common)
Supplements:    ((grub2 or grub2-common) and branding-%{theme_name})
Conflicts:      grub2-branding
Conflicts:      grub2-branding-openSUSE
Provides:       grub2-branding = %{version}
BuildArch:      noarch
%if 0%{?update_bootloader_requires:1}
%{update_bootloader_requires}
%endif

%description -n grub2-branding-%{theme_name}
%{theme_name} %{theme_version_clean} branding for the GRUB2's graphical console
%endif

%package -n plymouth-branding-%{theme_name}
Summary:        %{theme_name} %{theme_version_clean} branding for Plymouth bootsplash
License:        GPL-2.0-or-later
BuildRequires:  plymouth-theme-veles
Requires:       plymouth-scripts
Requires:       plymouth-theme-veles
Supplements:    (plymouth and branding-%{theme_name})
Conflicts:      plymouth-branding
Conflicts:      plymouth-branding-openSUSE
Provides:       plymouth-branding = %{version}
BuildArch:      noarch

%description -n plymouth-branding-%{theme_name}
%{theme_name} %{theme_version_clean} branding for the plymouth bootsplash

%prep
%autosetup -p1 -n branding-%{theme_version}

%build
%make_build

%install
%make_install

%if 0%{?suse_version} >= 1550
mkdir -p %{buildroot}/%{_distconfdir}
mv %{buildroot}/%{_sysconfdir}/Veles-brand %{buildroot}/%{_distconfdir}
%endif

%if 0%{?grub2} < 1
rm -rf %{buildroot}%{_datadir}/grub2
%endif

%if 0%{?grub2} > 0
%post -n grub2-branding-%{theme_name}
%{_datadir}/grub2/themes/%{theme_name}/activate-theme
%if 0%{?update_bootloader_check_type_refresh_post:1}
%{update_bootloader_check_type_refresh_post grub2 grub2-efi}
%else
if test -e /boot/grub2/grub.cfg ; then
  %{_sbindir}/grub2-mkconfig -o /boot/grub2/grub.cfg || true
fi
%endif

%posttrans -n grub2-branding-%{theme_name}
%{?update_bootloader_posttrans}

%postun -n grub2-branding-%{theme_name}
if [ $1 = 0 ] ; then
  rm -rf /boot/grub2/themes/%{theme_name}
fi
%endif

%files
# %license LICENSE
%if 0%{?suse_version} >= 1550
%{_distconfdir}/Veles-brand
%else
%config %{_sysconfdir}/Veles-brand
%endif


%if 0%{?grub2} > 0
%files -n grub2-branding-%{theme_name}
%{_datadir}/grub2
%dir /boot/grub2
%dir /boot/grub2/themes
%ghost /boot/grub2/themes/%{theme_name}
%endif

%files -n plymouth-branding-%{theme_name}
%dir %{_datadir}/plymouth
%{_datadir}/plymouth/plymouthd.defaults

%changelog
