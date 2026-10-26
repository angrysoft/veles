%define sway_version %(rpm -q --queryformat "%%{version}" sway)


Name:           veles-desktop
Version:        0.1.0
Release:        0
Summary:        The Veles desktop environment meta package
License:        MIT
Group:          Metapackages
URL:            https://github.com/angrysoft/veles
Source0:        %{name}.tar.gz
Source1:        veles-desktop.rpmlintrc

BuildArch:      noarch
BuildRequires:  pkgconfig(systemd)

# system
Requires:       veles-base
Requires:       command-not-found

# basic DE
Requires:       vls-shell
Requires:       regreet
Requires:       pipewire
Requires:       wireplumber
Requires:       foot
Requires:       foot-extra-terminfo
Requires:       blueman
Requires:       blueman-lang
Requires:       udiskie
Requires:       udiskie-lang
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

#BRAND: /etc/greetd/config, /etc/greetd/sway-config,
#BRAND: and /etc/greetd/regreet.toml contain Veles config and branding

%description -n greetd-branding-Veles
This package provides the Veles look and feel for greetd.

%prep
%setup -q -c -n %{name}

%build

%install

## greetd
install -D -p -m 644 greetd/config.toml     %{buildroot}%{_sysconfdir}/greetd/config.toml
install -D -p -m 644 greetd/regreet.toml       %{buildroot}%{_sysconfdir}/greetd/veles-regreet.toml
install -D -p -m 644 greetd/sway-config     %{buildroot}%{_sysconfdir}/greetd/sway-config

## Sway
install -D -p -m 644 config/sway/config %{buildroot}%{_sysconfdir}/sway/config
install -D -p -m 644 config/sway/env %{buildroot}%{_sysconfdir}/sway/env

install -D -p -m 644 session/vls-session.target %{buildroot}%{_prefix}/lib/systemd/user/vls-session.target
install -D -p -m 644 session/vls-session-shutdown.target %{buildroot}%{_prefix}/lib/systemd/user/vls-session-shutdown.target
install -D -p -m 644 session/sway.service %{buildroot}%{_prefix}/lib/systemd/user/sway.service
install -D -p -m 644 session/vls-shell.service %{buildroot}%{_prefix}/lib/systemd/user/vls-shell.service
install -D -p -m 644 session/vls-shell.desktop %{buildroot}%{_datadir}/wayland-sessions/vls-shell.desktop.brand
install -D -p -m 755 session/vls-run.sh %{buildroot}%{_bindir}/vls-run.sh
install -D -p -m 644 session/50-vls-shell.preset %{buildroot}%{_prefix}/lib/systemd/user-preset/50-vls-shell.preset

### foot
install -D -p -m 644 config/foot/foot.ini %{buildroot}%{_sysconfdir}/foot/foot.ini
install -D -p -m 644 config/foot/foot-colors.ini %{buildroot}%{_sysconfdir}/foot/foot-colors.ini

# %pre -n veles-desktop
# %service_add_pre sway.service vls-shell.service

%post -n veles-desktop
test -e %{_datadir}/wayland-sessions/vls-shell.desktop && \
    mv -n %{_datadir}/wayland-sessions/vls-shell.desktop %{_datadir}/wayland-sessions/vls-shell.desktop.orig || true
cp %{_datadir}/wayland-sessions/vls-shell.desktop.brand %{_datadir}/wayland-sessions/vls-shell.desktop
# %service_add_post sway.service vls-shell.service

# %preun -n veles-desktop
# %service_del_preun sway.service vls-shell.service

%postun -n veles-desktop
test -e %{_datadir}/wayland-sessions/vls-shell.desktop.orig && \
    mv %{_datadir}/wayland-sessions/vls-shell.desktop.orig %{_datadir}/wayland-sessions/vls-shell.desktop || true
# %service_del_postun sway.service vls-shell.service

%files -n greetd-branding-Veles
%dir %{_sysconfdir}/greetd/
%attr(644,greeter,greeter) %config(noreplace) %{_sysconfdir}/greetd/config.toml
%attr(644,greeter,greeter) %config(noreplace) %{_sysconfdir}/greetd/sway-config
%attr(644,greeter,greeter) %config(noreplace) %{_sysconfdir}/greetd/veles-regreet.toml

    
%files -n sway-branding-Veles
%dir %{_sysconfdir}/sway
%config %{_sysconfdir}/sway/config
%config %{_sysconfdir}/sway/env

%files -n veles-desktop
%{_prefix}/lib/systemd/user/vls-session.target
%{_prefix}/lib/systemd/user/vls-session-shutdown.target
%{_prefix}/lib/systemd/user/sway.service
%{_prefix}/lib/systemd/user/vls-shell.service
%{_datadir}/wayland-sessions/vls-shell.desktop.brand
%{_bindir}/vls-run.sh
%{_prefix}/lib/systemd/user-preset/50-vls-shell.preset

%dir %{_sysconfdir}/foot
%config(noreplace) %{_sysconfdir}/foot/foot.ini
%config(noreplace) %{_sysconfdir}/foot/foot-colors.ini


%changelog