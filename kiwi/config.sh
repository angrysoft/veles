#!/bin/bash

# systemctl enable getty@tty1.service

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
}


setup_target_rootfs() {
    echo "LOG: Konfiguracja dla profilu TargetRootfs (docelowy system)"
    systemctl set-default graphical.target
    systemctl enable NetworkManager.service
    systemctl enable systemd-timesyncd.service
    systemctl enable getty@tty1.service
    
    # Czyszczenie cache menedżera pakietów, by odchudzić docelowy obraz .img
    if command -v zypper &> /dev/null; then
        zypper clean -a
    fi
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