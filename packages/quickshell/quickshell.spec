#
# spec file for package quickshell
#
# Copyright (c) 2026 Sebastian Zwierzchowski
#

Name:           quickshell
Version:        0.3.2
Release:        0
Summary:        Flexible QtQuick based desktop shell
License:        GPL-3.0-or-later
URL:            https://git.outfoxxed.me/quickshell/quickshell
Source0:        v%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Qml)
BuildRequires:  cmake(Qt6ShaderTools)
BuildRequires:  cmake(Qt6WaylandClient)
BuildRequires:  cmake(Qt6Svg)
BuildRequires:  ninja
BuildRequires:  pkg-config
BuildRequires:  gcc-c++
BuildRequires:  qt6-base-devel
BuildRequires:  qt6-base-private-devel
BuildRequires:  qt6-declarative-devel
BuildRequires:  qt6-declarative-private-devel
BuildRequires:  qt6-waylandclient-private-devel
BuildRequires:  qt6-shadertools-devel
BuildRequires:  qt6-wayland-devel
BuildRequires:  qt6-svg-devel
BuildRequires:  spirv-tools-devel
BuildRequires:  libdrm-devel
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  cli11-devel
BuildRequires:  cpptrace-devel
BuildRequires:  libdwarf-devel
BuildRequires:  libzstd-devel
BuildRequires:  Mesa-libGLESv3-devel
BuildRequires:  jemalloc-devel
BuildRequires:  pipewire-devel
BuildRequires:  pam-devel
BuildRequires:  libdrm-devel
BuildRequires:  libgbm-devel
BuildRequires:  Mesa-libEGL-devel
BuildRequires:  Mesa-libGLESv3-devel
BuildRequires:  polkit-devel
BuildRequires:  glib2-devel
BuildRequires:  fdupes

Requires:       qt6-base
Requires:       qt6-declarative
Requires:       qt6-wayland
Requires:       qt6-svg
Requires:       jemalloc
Requires:       wayland
Requires:       pipewire
Requires:       pam
Requires:       polkit

%description
Quickshell is a modern toolkit built with C++ for creating desktop interface
components — bars, widgets, lock screens, launchers, and complete environments
using QtQuick and QML with hot reload support.

%prep
%setup -n quickshell

%build
cmake -G Ninja -B build -W no-dev \
    -D CMAKE_BUILD_TYPE=Release \
    -D DISTRIBUTOR="Veles Linux" \
    -D CRASH_HANDLER=Off \
    -D CMAKE_INSTALL_PREFIX=/usr \
    -D CMAKE_SKIP_INSTALL_RPATH=ON \
    -D INSTALL_QML_PREFIX=%{_lib}/qt6/qml

cmake --build build

%install
DESTDIR=%{buildroot} cmake --install build
%fdupes %{buildroot}%{_libdir}/qt6/qml


%files
%license LICENSE
%doc README.md
%{_bindir}/quickshell
%{_bindir}/qs
%{_datadir}/applications/org.quickshell.desktop
%{_libdir}/qt6/qml/Quickshell
%dir %{_datadir}/icons/hicolor
%dir %{_datadir}/icons/hicolor/scalable
%dir %{_datadir}/icons/hicolor/scalable/apps
%{_datadir}/icons/hicolor/scalable/apps/org.quickshell.svg

%changelog
* Sun Oct 25 2026 Sebastian Zwierzchowski <sebastian@ves.local> - 0.3.2-0
- Initial package for openSUSE based on upstream build requirements