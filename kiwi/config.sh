#!/bin/bash
systemctl set-default multi-user.target

# systemctl enable getty@tty1.service
systemctl enable NetworkManager.service

setup_installer() {
    echo "LOG: Konfiguracja dla profilu Installer (LiveCD)"

    # /usr/share/polkit-1/rules.d/49-calamares.rules
    # polkit.addRule(function(action, subject) {
    #     if (action.id === "org.freedesktop.calamares.run" &&
    #         subject.isInGroup("live")) {
    #         return polkit.Result.YES;
    #     }
    # });

    systemctl disable getty@tty1.service
    systemctl enable calamares-installer.service
    # systemctl enable polkit.service
}


setup_target_rootfs() {
    echo "LOG: Konfiguracja dla profilu TargetRootfs (docelowy system)"
    # Wyłączenie usług, które nie powinny być aktywne domyślnie u użytkownika
        # lub konfiguracja bazowych usług systemowych
        systemctl enable NetworkManager.service
        systemctl enable systemd-timesyncd.service
        
        # Czyszczenie cache menedżera pakietów, by odchudzić docelowy obraz .img
        if command -v zypper &> /dev/null; then
            zypper clean -a
        fi


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