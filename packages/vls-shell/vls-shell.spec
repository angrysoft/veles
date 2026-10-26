Name: vls-shell
Version: 0.1.0
Release: 6
Summary: VLS shell package
License: Apache-2.0
Group:          System/GUI/Other
URL: https://github.com/angrysoft/vls-shell
Source0:        %{name}.tar.gz

BuildRequires:  go
BuildRequires:  make

Requires:  sway
Requires:  quickshell

%description
Veles wayland desktop shell package

%prep
%autosetup -p1 -n %{name}-main

%build
%make_build

%install
%make_install

%files
%{_bindir}/vlsmsg
%{_datadir}/vls-shell/
%{_datadir}/applications/

%changelog

