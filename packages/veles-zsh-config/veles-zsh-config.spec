#
# spec file for package veles-base
#
# Copyright (c) 2026 Angrysoft Sebastian Zwierzchowski <sebastian.zwierzchowski@gmail.com>
#
# SPDX-License-Identifier: MIT
#

Name:           veles-zsh-config
Version:        0.1.0
Release:        1
Summary:        Global Zsh configuration and aliases for Veles Linux
License:        MIT
BuildArch:      noarch


Requires:   zsh

Source0:    zsh.zshrc.local
Source1:    prompt_veles_setup
Source2:    skel.zshrc

%description
Global Zsh environment configuration, prompts, and default aliases for Veles Linux.

%prep

%build

%install
install -Dm 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/zsh.zshrc.local
install -Dm 644 %{SOURCE1} %{buildroot}%{_datadir}/zsh/functions/Prompts/prompt_veles_setup
install -Dm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/skel/.zshrc

%files
%{_sysconfdir}/zsh.zshrc.local
%dir %{_datadir}/zsh
%dir %{_datadir}/zsh/functions
%dir %{_datadir}/zsh/functions/Prompts
%{_datadir}/zsh/functions/Prompts/prompt_veles_setup
%{_sysconfdir}/skel/.zshrc

%changelog
* Sat May 16 2026 AngrySoft <sebastian.zwierzchowski@gmail.com>
- Initial veles-release package