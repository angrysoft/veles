Name:           mangowc
Version:        0.18.5
Release:        0
Summary:        Wayland compositor base wlroots and scenefx(dwm but wayland)
License:        (MIT and GPL-3.0-only and CC0-1.0)
URL:            https://mangowm.github.io/
Source0:        mango-%{version}.tar.gz
BuildRequires:  gcc-c++
BuildRequires:  hicolor-icon-theme
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libseat)
BuildRequires:  pkgconfig(libpcre2-8)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(scenefx-0.5)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(wlroots-0.20)
BuildRequires:  pkgconfig(xwayland)
BuildRequires:  pkgconfig(libcjson)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(systemd)
Recommends:     xwayland
Recommends:     foot
Suggests:       grim
BuildRequires:  meson
BuildSystem:    meson
Requires:       %{name}-branding

%description
mangowm is a lightweight and feature-rich Wayland compositor.

%package branding-upstream
Summary:        Upstream branding of %{name}
Group:          System/GUI/Other
Requires:       %{name} = %{version}
Supplements:    (%{name} and branding-upstream)
Conflicts:      %{name}-branding
Provides:       %{name}-branding = %{version}
BuildArch:      noarch
#BRAND: /etc/mango/config.conf contains upstream config and brand

%description branding-upstream
This package provides the upstream look and feel for mangowm.

%prep
%autosetup -n mango-%{version}

%build
%meson -Db_pie=true
%meson_build

%check
%meson_test

%install
%meson_install

%files
%license LICENSE
%doc README.md
%{_bindir}/mango
%{_bindir}/mmsg
%{_bindir}/mangonag
%{_mandir}/man1/mmsg.1*
%{_mandir}/man1/mangonag.1*
%{_userunitdir}/mango-session.target
%dir %{_datadir}/wayland-sessions
%{_datadir}/wayland-sessions/mango.desktop
%dir %{_datadir}/xdg-desktop-portal
%{_datadir}/xdg-desktop-portal/mango-portals.conf

%files branding-upstream
%dir %{_sysconfdir}/mango
%config(noreplace) %{_sysconfdir}/mango/config.conf
%config(noreplace) %{_sysconfdir}/mango/config.toml

%changelog
