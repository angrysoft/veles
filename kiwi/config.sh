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

#add vendor
    cat <<EOF > /etc/zypp/vendors.d/00-veles.repo
[main]
vendors=Veles,obs://build.opensuse.org/home:angrysoft,openSUSE
EOF
    zypper --gpg-auto-import-keys refresh
}

create_sway_live_config() {
    echo "LOG: Generowanie konfiguracji Sway dla profilu Installer (LiveCD)"
    # Przykładowa implementacja, dostosuj do swoich potrzeb
    mkdir -p /home/live/.config/sway
    cat <<EOF > /home/live/.config/sway/config
    # outputs
output * enable bg #19120c solid_color

# no decorations
default_border none
hide_edge_borders both

# disable mouse focus
focus_follows_mouse no

# autostart
exec pkexec calamares
EOF
    chown -R live:live /home/live/.config/sway
}


set_autologin() {
    echo "LOG: Generowanie skryptu uruchamiającego instalator Calamares dla profilu Installer (LiveCD)"
    # Przykładowa implementacja, dostosuj do swoich potrzeb
#cat <<EOF >> /etc/greetd/config.toml
#[initial_session]
#command = "sway"
#user = "live"
#EOF
mkdir -p /etc/systemd/system/getty@tty1.service.d
cat <<EOF > /etc/systemd/system/getty@tty1.service.d/autologin.conf
[Service]
ExecStart=
ExecStart=-/usr/bin/agetty --noreset --noclear --autologin live - ${TERM}
EOF

cat <<EOF > /home/live/.bash_profile
if [ -z "$DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then
    exec sway
    # press any to reboot
        read -n 1 -s -r -p "Press any key to reboot..."
        systemctl reboot
fi
EOF
}


installer_polkit() {
    echo "LOG: Konfiguracja Polkit dla profilu Installer (LiveCD)"

cat <<EOF > /etc/polkit-1/rules.d/49-calamares.rules
polkit.addRule(function(action, subject) {
    if (action.id === "io.calamares.calamares.pkexec.run" &&
        subject.user === "live") {
        return polkit.Result.YES;
    }
});
EOF
}
 

setup_installer() {
    echo "LOG: Konfiguracja dla profilu Installer (LiveCD)"

    systemctl set-default multi-user.target
    systemctl enable NetworkManager.service
    systemctl enable getty@tty1.service
    generate_repos_files
    zypper clean -a
    set_autologin
    installer_polkit
    create_sway_live_config
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
