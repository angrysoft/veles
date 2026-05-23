#!/bin/bash

# systemctl enable getty@tty1.service

generate_repos_files() {
    echo "LOG: Generowanie plików repozytoriów dla KIWI..."
    # Przykładowa implementacja, dostosuj do swoich potrzeb
    # Możesz użyć szablonów lub wygenerować pliki na podstawie zmiennych środowiskowych
    cat <<EOF > /etc/zypp/repos.d/oss.repo
[oss]
name=Repozytorium OSS
enabled=1
autorefresh=1
baseurl=http://download.opensuse.org/tumbleweed/repo/oss
path=/
type=rpm-md
keeppackages=0
priority=10
EOF

    cat <<EOF > /etc/zypp/repos.d/non-oss.repo
[non-oss]
name=Repozytorium Non-OSS
enabled=1
autorefresh=1
baseurl=http://download.opensuse.org/tumbleweed/repo/non-oss
path=/
type=rpm-md
keeppackages=0
priority=10
EOF

    cat <<EOF > /etc/zypp/repos.d/update.repo
[update]
name=Repozytorium aktualizacji
enabled=1
autorefresh=1
baseurl=http://download.opensuse.org/update/tumbleweed
path=/
type=rpm-md
keeppackages=0
priority=10
EOF

    cat <<EOF > /etc/zypp/repos.d/veles.repo
[veles]
name=Repozytorium Veles
enabled=1
autorefresh=1
baseurl=https://download.opensuse.org/repositories/home:/angrysoft/openSUSE_Tumbleweed/
path=/
type=rpm-md
keeppackages=0
priority=1
EOF
}

setup_installer() {
    echo "LOG: Konfiguracja dla profilu Installer (LiveCD)"

    # /usr/share/polkit-1/rules.d/49-calamares.rules
    # polkit.addRule(function(action, subject) {
    #     if (action.id === "org.freedesktop.calamares.run" &&
    #         subject.isInGroup("live")) {
    #         return polkit.Result.YES;
    #     }
    # });

    systemctl set-default multi-user.target
    systemctl enable NetworkManager.service
    #systemctl enable getty@tty1.service
    systemctl enable calamares-installer.service
    # systemctl enable polkit.service
    generate_repos_files
    zypper clean -a
}


setup_target_rootfs() {
    echo "LOG: Konfiguracja dla profilu TargetRootfs (docelowy system)"
    systemctl set-default graphical.target
    systemctl enable NetworkManager.service
    systemctl enable systemd-timesyncd.service
    systemctl enable getty@tty1.service
    generate_repos_files
    zypper clean -a
}


echo "LOG: Uruchamianie skryptu konfiguracyjnego KIWI..."
echo "LOG: Aktywne profile: $kiwi_profiles"

# Sprawdzamy profil główny (w dopasowaniu używamy * na wypadek wielu profili)
case " $kiwi_profiles " in
    *" Installer "*)
        setup_installer
        ;;

    *" TargetRootfs "*)
        setup_target_rootfs
        ;;

    *)
        echo "WAR: Nie rozpoznano profilu lub budowany jest profil domyślny!"
        ;;
esac
exit 0
