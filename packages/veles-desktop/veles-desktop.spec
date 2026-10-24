%define sway_version %(rpm -q --queryformat "%%{version}" sway)


Name:           veles-desktop
Version:        0.1.0
Release:        0
Summary:        The Veles desktop environment meta package
License:        MIT
Group:          Metapackages
URL:            https://github.com/angrysoft/veles
Source0:        https://github.com/angrysoft/veles/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        veles-desktop.rpmlintrc

BuildArch:      noarch
BuildRequires:  pkgconfig(systemd)

# system
Requires:       veles-base
Requires:       command-not-found

# basic DE
Requires:       (gtkgreet or wlgreet)
Requires:       pipewire
Requires:       wireplumber
Requires:       foot
Requires:       foot-extra-terminfo
Recommends:     grim
Recommends:     slurp
Recommends:     chromium
Recommends:     bluetuith
Suggests:       mpv
Suggests:       imv

# branding
Requires:       sway-branding-Veles
# Requires:       greetd-branding-openSUSE
%ifarch x86_64 %{ix86}
Requires:       gfxboot-branding-Veles
%endif

# xdg portals and utils
Requires:       xdg-desktop-portal
Requires:       xdg-desktop-portal-wlr
Requires:       xdg-desktop-portal-gtk
Requires:       xdg-utils

# Appearance
Requires:       papirus-icon-theme
Requires:       metatheme-adwaita-common
# Recommends:     qt6-qtwayland
# Recommends:     qt6ct
Recommends:     adwaita-qt6

# Fonts
Requires:       adobe-sourcecodepro-fonts
Requires:       adobe-sourcesanspro-fonts
Requires:       adobe-sourceserifpro-fonts
Requires:       dejavu-fonts
Requires:       ghostscript-fonts-other
Requires:       ghostscript-fonts-std
Requires:       google-carlito-fonts
Requires:       google-droid-fonts
Requires:       google-opensans-fonts
Requires:       google-roboto-fonts
Requires:       noto-coloremoji-fonts
Requires:       noto-emoji-fonts
Requires:       noto-sans-fonts
Requires:       cantarell-fonts
Requires:       jetbrains-mono-fonts

%description
This meta-package aggregates Veles desktop environment packages.
It includes essential system utilities, basic desktop environment components, branding, xdg portals, appearance settings, and fonts required for a complete desktop experience.

%package -n     sway-branding-Veles
Summary:        Veles branding of sway
Group:          System/GUI/Other
BuildRequires:  sway
Requires:       brightnessctl
Requires:       fontawesome-fonts
Requires:       jq
Requires:       patterns-sway-sway
Requires:       polkit-gnome
Requires:       polkit-default-privs
Requires:       sway
Requires:       wallpaper-branding-Veles
Provides:       sway-branding = %{version}
Conflicts:      sway-branding
Supplements:    (sway and branding-Veles)

#BRAND: /etc/sway/config and /etc/sway/config.d/
#BRAND: contain Veles config and branding

%description -n sway-branding-Veles
This package provides the Veles look and feel for sway.

## Sway
install -D -p -m 644 config/sway/config %{buildroot}%{_sysconfdir}/sway/config
install -D -p -m 644 config/sway/env %{buildroot}%{_sysconfdir}/sway/env
# install -D -p -m 644 config/sway/config.d/50-openSUSE.conf %{buildroot}%{_sysconfdir}/sway/config.d/50-openSUSE.conf
# install -D -p -m 644 config/sway/config.d/55-openSUSE-windows.conf %{buildroot}%{_sysconfdir}/sway/config.d/55-openSUSE-windows.conf

install -D -p -m 644 sway/sway-session.target %{buildroot}%{_prefix}/lib/systemd/user/sway-session.target
install -D -p -m 644 sway/sway.service %{buildroot}%{_prefix}/lib/systemd/user/sway.service
install -D -p -m 644 sway/sway.desktop %{buildroot}%{_datadir}/wayland-sessions/sway.desktop.brand
install -D -p -m 755 sway/sway-session.sh %{buildroot}%{_bindir}/sway-session.sh

### foot
# so far doesn't have special branding package and it doesn't support system wide config
install -D -p -m 644 config/foot/foot.ini %{buildroot}%{_sysconfdir}/foot/foot.ini
install -D -p -m 644 config/foot/foot-colors.ini %{buildroot}%{_sysconfdir}/foot/foot-colors.ini


# %files -n greetd-branding-openSUSE
# %dir %{_sysconfdir}/greetd/
# %attr(644,greeter,greeter) %config(noreplace) %{_sysconfdir}/greetd/config.toml
# %attr(644,greeter,greeter) %config(noreplace) %{_sysconfdir}/greetd/sway-config
# %attr(644,greeter,greeter) %config(noreplace) %{_sysconfdir}/greetd/environments
# %attr(644,greeter,greeter) %config(noreplace) %{_sysconfdir}/greetd/style.css

    
%files -n sway-branding-Veles
%dir %{_sysconfdir}/sway
%config %{_sysconfdir}/sway/config
%config %{_sysconfdir}/sway/env
%dir %{_sysconfdir}/sway/config.d
%config %{_sysconfdir}/sway/config.d/50-openSUSE.conf
%config %{_sysconfdir}/sway/config.d/55-openSUSE-windows.conf
%{_prefix}/lib/systemd/user/sway-session.target
%{_prefix}/lib/systemd/user/sway.service
%{_datadir}/wayland-sessions/sway.desktop.brand
%{_bindir}/sway-session.sh

%dir %{_sysconfdir}/foot
%config(noreplace) %{_sysconfdir}/foot/foot.ini
%config(noreplace) %{_sysconfdir}/foot/foot-colors.ini


%changelog