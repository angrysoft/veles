%define sway_version %(rpm -q --queryformat "%%{version}" sway)


Name:           veles-desktop
Version:        0.2.0
Release:        0
Summary:        The Veles desktop environment meta package
License:        MIT
Group:          Metapackages
URL:            https://github.com/angrysoft/veles
Source0:        veles-desktop.rpmlintrc
Source1:        foot.ini
Source2:        foot-colors.ini
Source3:        sway-config
Source4:        sway-env
Source5:        greetd.preset
Source6:        greetd.config.toml
Source7:        greetd.greetd.pam
Source8:        greetd.tuigreet.toml
Source9:        sway.service
Source10:       vls-session.target
Source11:       vls-session-shutdown.target
Source12:       vls-shell.service
Source13:       vls-shell.desktop

BuildArch:      noarch
BuildRequires:  pkgconfig(systemd)

# system
Requires:       veles-base
Requires:       command-not-found

# basic DE
Requires:       vls-shell
Requires:       greetd
Requires:       tuigreet
Requires:       pipewire
Requires:       wireplumber
Requires:       foot
Requires:       foot-extra-terminfo
Requires:       blueman
Requires:       blueman-lang
Requires:       udiskie
Requires:       udiskie-lang
Requires:       NetworkManager-applet
Requires:       gnome-keyring
Requires:       wl-clipboard
Requires:       cliphist
Recommends:     grim
Recommends:     slurp
Recommends:     chromium
Suggests:       mpv
Suggests:       imv

# branding
Requires:       sway-branding-Veles
Requires:       greetd-branding-Veles
%ifarch x86_64 %{ix86}
Requires:       gfxboot-branding-Veles
%endif

# xdg portals and utils
Requires:       xdg-desktop-portal
Requires:       xdg-desktop-portal-wlr
Requires:       xdg-desktop-portal-gtk
Requires:       xdg-user-dirs
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
Requires:       polkit-gnome
Requires:       polkit-default-privs
Requires:       sway
Provides:       sway-branding = %{version}
Conflicts:      sway-branding
Supplements:    (sway and branding-Veles)

#BRAND: /etc/sway/config and /etc/sway/config.d/
#BRAND: contain Veles config and branding

%description -n sway-branding-Veles
This package provides the Veles look and feel for sway.

%package -n     greetd-branding-Veles
Summary:        Veles branding of greetd
Group:          System/Management
BuildRequires:  greetd
Provides:       greetd-branding = %{version}
Conflicts:      greetd-branding
Supplements:    (greetd and branding-Veles)

#BRAND: /etc/greetd/config.toml, /etc/greetd/tuigreet.toml
#BRAND: contain Veles config and branding

%description -n greetd-branding-Veles
This package provides the Veles look and feel for greetd.

%prep


%build

%install
## greetd
install -D -p -m 644 %{SOURCE5} %{buildroot}%{_libdir}/systemd/system-preset/50-greetd.preset
install -D -p -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/greetd/config.toml
install -D -p -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/pam.d/greetd
install -D -p -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/greetd/tuigreet.toml

## Sway
install -D -p -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sway/config
install -D -p -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sway/env

install -D -p -m 644 %{SOURCE9} %{buildroot}%{_prefix}/lib/systemd/user/sway.service
install -D -p -m 644 %{SOURCE10} %{buildroot}%{_prefix}/lib/systemd/user/vls-session.target
install -D -p -m 644 %{SOURCE11} %{buildroot}%{_prefix}/lib/systemd/user/vls-session-shutdown.target
install -D -p -m 644 %{SOURCE12} %{buildroot}%{_prefix}/lib/systemd/user/vls-shell.service
install -D -p -m 644 %{SOURCE13} %{buildroot}%{_datadir}/wayland-sessions/vls-shell.desktop

### foot
install -D -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/foot/foot.ini
install -D -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/foot/foot-colors.ini

%pre -n greetd-branding-Veles
%service_add_pre greetd.service

%post -n greetd-branding-Veles
%service_add_post greetd.service

%preun -n greetd-branding-Veles
%service_del_preun greetd.service

%postun -n greetd-branding-Veles
%service_del_postun greetd.service

%files -n greetd-branding-Veles
%dir %{_sysconfdir}/greetd/
%attr(644,greeter,greeter) %config(noreplace) %{_sysconfdir}/greetd/config.toml
%attr(644,greeter,greeter) %config(noreplace) %{_sysconfdir}/greetd/tuigreet.toml

    
%files -n sway-branding-Veles
%dir %{_sysconfdir}/sway
%config %{_sysconfdir}/sway/config
%config %{_sysconfdir}/sway/env

%files -n veles-desktop
%{_prefix}/lib/systemd/user/vls-session.target
%{_prefix}/lib/systemd/user/vls-session-shutdown.target
%{_prefix}/lib/systemd/user/sway.service
%{_prefix}/lib/systemd/user/vls-shell.service
%{_datadir}/wayland-sessions/vls-shell.desktop
%{_sysconfdir}/pam.d/greetd
%{_libdir}/systemd/system-preset/50-greetd.preset

%dir %{_sysconfdir}/foot
%config %{_sysconfdir}/foot/foot.ini
%config %{_sysconfdir}/foot/foot-colors.ini


%changelog