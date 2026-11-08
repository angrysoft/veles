Name: vls-shell
Version: 0.2.0
Release: 1
Summary: VLS shell package
License: Apache-2.0
Group:          System/GUI/Other
URL: https://github.com/angrysoft/vls-shell
Source0:        %{name}.tar.gz
Source1:        veles-shell-lock.pam

BuildRequires:  go
BuildRequires:  make

Requires:  mangowm
Requires:  wlopm
Requires:  quickshell
Requires:  upower
Requires:  upower-lang
Requires:  tuned
Requires:  tuned-ppd

%description
Veles wayland desktop shell package

%prep
%autosetup -p1 -n %{name}-main

%build
%make_build

%install
install -D -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/veles-shell-lock
%make_install

%files
%{_bindir}/vlsmsg
%{_datadir}/vls-shell/
%{_datadir}/pixmaps/
%{_datadir}/applications/
%{_datadir}/wallpapers/
%{_sysconfdir}/pam.d/veles-shell-lock

%changelog

