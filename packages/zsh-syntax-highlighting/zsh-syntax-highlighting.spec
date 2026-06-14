%global debug_package %{nil}

Name:     zsh-syntax-highlighting    
Version:  0.8.0
Release:  1%{?dist}
Summary:  Fish shell like syntax highlighting for Zsh.

Group:    Development/Tools
License:  BSD-3-Clause
URL:      https://github.com/zsh-users/%{name}
Source0:  https://github.com/zsh-users/%{name}/archive/%{version}.tar.gz

Requires: zsh

%description
Fish shell like syntax highlighting for Zsh.

%prep
%autosetup

%build	
%set_build_flags
%make_build

%install
%make_install DESTDIR=%{buildroot} PREFIX=/usr

%files
%defattr(-,root,root,-)
%license COPYING.md
/usr/share/zsh-syntax-highlighting/
/usr/share/doc/zsh-syntax-highlighting/

%changelog
* Sun Jun 14 2026 AngrySoft <sebastian.zwierzchowski@gmail.com> - 0.8.0-1
- Initial package 0.8.0