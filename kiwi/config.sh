#!/bin/bash


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

create_sway_calamares_autostart() {
    echo "LOG: Generowanie konfiguracji Sway dla uruchamiania Calamares"
    # Przykładowa implementacja, dostosuj do swoich potrzeb
    mkdir -p /home/live/.config/sway/config.d
    cat <<EOF > /home/live/.config/sway/config.d/calamares
    # autostart
    exec pkexec env DISPLAY=\$DISPLAY WAYLAND_DISPLAY=\$WAYLAND_DISPLAY XDG_RUNTIME_DIR=\$XDG_RUNTIME_DIR calamares
EOF
    
    chown -R live:users /home/live/.config/sway
}


set_autologin() {
    echo "LOG: Generowanie skryptu uruchamiającego instalator Calamares dla profilu Installer (LiveCD)"
mkdir -p /etc/systemd/system/getty@tty1.service.d
cat <<EOF > /etc/systemd/system/getty@tty1.service.d/override.conf
[Service]
ExecStart=
ExecStart=-/usr/sbin/agetty --autologin live --noclear %I linux
EOF

cat <<EOF >> /home/live/.zshrc

if [ "$(tty)" = "/dev/tty1" ]; then
    systemctl --user start --wait vls-session.target
    # press any to reboot
        read "?Press any key to reboot..."
        systemctl reboot
fi
EOF
}
 
echo "LOG: Konfiguracja  (LiveCD)"

systemctl set-default graphical.target
systemctl enable NetworkManager.service
systemctl enable getty@tty1.service
systemctl enable systemd-timesyncd.service
# systemctl enable greetd.service

# --- BEZPIECZNE WYŁĄCZENIE SNAPPERA DLA LIVE ISO ---
echo "LOG: Wyłączanie usług Snappera dla środowiska Live"
systemctl disable snapper-timeline.timer || true
systemctl disable snapper-cleanup.timer || true
systemctl disable snapper-boot.service || true
# Czyszczenie domyślnych konfiguracji Snappera z obrazu live
rm -rf /etc/snapper/configs/*
# ----------------------------------------------------

generate_repos_files
zypper clean -a
set_autologin
installer_polkit
create_sway_calamares_autostart
