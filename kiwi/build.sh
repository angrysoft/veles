#!/bin/sh
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

PROJECT_DIR="${SCRIPT_DIR}/tmp"
TARGET_BUILD_DIR="${PROJECT_DIR}/build/target"
LIVE_BUILD_DIR="${PROJECT_DIR}/build/live"
OVERLAY_IMG_DIR="${SCRIPT_DIR}/root/usr/share/veles-images"
RM="rm -vrf"
MKDIR="mkdir -pv"
CP="cp -v"


check_root() {
    if [ "$(id -u)" -ne 0 ]; then
        echo "Ten skrypt musi być uruchomiony jako root lub za pomocą run0."
        exit 1
    fi
}

gen_polkit_helper() {
    echo "LOG: Generowanie pliku reguł Polkit dla Calamares"
cat <<EOF >${SCRIPT_DIR}/49-run0-cache.rules
polkit.addRule(function(action, subject) {
       if (action.id == "org.freedesktop.systemd1.manage-units" || 
           action.id == "org.freedesktop.policykit.exec") {
           if (subject.isInGroup("wheel")) {
               return polkit.Result.AUTH_ADMIN_KEEP;
           }
       }
   });
EOF
cp "${SCRIPT_DIR}/49-run0-cache.rules" /etc/polkit-1/rules.d/
}

# gen_polkit_helper

check_root

echo "=== KROK 1: Czyszczenie starych plików budowy ==="
$RM "${PROJECT_DIR}"
$RM "${SCRIPT_DIR}/root"
$MKDIR "${TARGET_BUILD_DIR}" "${LIVE_BUILD_DIR}" "${OVERLAY_IMG_DIR}"

echo "=== KROK 2: Budowanie profilu TargetRootfs (.squashfs) ==="
kiwi-ng --profile=TargetRootfs system build \
    --description "." \
    --target-dir "${TARGET_BUILD_DIR}"

GENERATED_IMG=$(ls "${TARGET_BUILD_DIR}"/*.squashfs | head -n 1)

echo "=== KROK 3: Kopiowanie obrazu do struktury overlay ==="
echo "Kopiuję: ${GENERATED_IMG}"
echo "Do: ${OVERLAY_IMG_DIR}/system-rootfs.squashfs"

# Kopiujemy pod stałą nazwą, którą wcześniej wpisaliśmy do unpackfs.conf
$CP "${GENERATED_IMG}" "${OVERLAY_IMG_DIR}/system-rootfs.squashfs"

echo "=== KROK 4: Budowanie profilu LiveISO (.iso) ==="
kiwi-ng --profile=Installer system build \
    --description "." \
    --target-dir "${LIVE_BUILD_DIR}"

echo "================================================="
echo "SUKCES! Twój instalacyjny obraz ISO znajduje się w:"
echo "${LIVE_BUILD_DIR}/"
echo "================================================="

