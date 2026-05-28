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
zypper --gpg-auto-import-keys refresh
}

gen_sway_live_config() {
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
exec calamares && swaymsg exit
EOF
    chown -R live:live /home/live/.config/sway
}

gen_run_installer() {
    echo "LOG: Generowanie skryptu uruchamiającego instalator Calamares dla profilu Installer (LiveCD)"
    # Przykładowa implementacja, dostosuj do swoich potrzeb
    cat <<EOF > /usr/local/bin/run_installer.sh
#!/bin/bash
# Skrypt uruchamiający instalator Calamares
calamares
if [ $? -ne 0 ]; then
    echo "Błąd: Nie można uruchomić instalatora Calamares!"
    exit 1
fi
systemctl reboot
EOF
    chmod +x /usr/local/bin/run_installer.sh
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
    systemctl enable getty@tty1.service
    #systemctl enable calamares-installer.service
    generate_repos_files
    zypper clean -a
cat <<EOF > /etc/systemd/system/getty@tty1.service.d/autologin.conf
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin live --noclear %I $TERM
EOF 
    
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
