#
# spec file for package scenefx
#

%define sover   5
%define libname libscenefx0_%{sover}
Name:           scenefx
Version:        0.5
Release:        0
Summary:        A drop-in wlroots replacement that allows eye-candy effects
License:        MIT
Group:          System/GUI/Other
URL:            https://github.com/wlrfx/scenefx
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wlroots-0.20)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(pixman-1)


%description
SceneFX is a project that takes the scene api and replaces the wlr
renderer with our own fx renderer, capable of rendering surfaces
with eye-candy effects including blur, shadows, and rounded
corners, while maintaining the benefits of simplicity gained from
using the scene api.

%package devel
Summary:        Development libraries for %{name}
Group:          Development/Libraries/C and C++
Requires:       %{libname} = %{version}

%description devel
This package provides all the necessary files for development with %{name}

%package -n %{libname}
Summary:        Shared libraries for %{name}
Group:          System/Libraries

%description -n %{libname}
This package provides the %{name} shared library.

%prep
%autosetup -p1

%build
%meson \
    -Dexamples=false \
    -Dwerror=false
%meson_build

%install
%meson_install

%post   -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files devel
%license LICENSE
%doc README.md
%{_includedir}/%{name}-0.%{sover}
%{_libdir}/pkgconfig/%{name}-0.%{sover}.pc

%files -n %{libname}
%{_libdir}/lib%{name}-0.%{sover}.so

%changelog
