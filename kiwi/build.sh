#!/bin/sh
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

PROJECT_DIR="${SCRIPT_DIR}/tmp"
TARGET_BUILD_DIR="${PROJECT_DIR}/build/target"
LIVE_BUILD_DIR="${PROJECT_DIR}/build/live"
OVERLAY_IMG_DIR="${SCRIPT_DIR}/root/usr/share/veles-images"


run_root() {
    if command -v run0 >/dev/null 2>&1; then
        run0 -D "${SCRIPT_DIR}" "$@"
    else
        sudo "$@"
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
run_root cp "${SCRIPT_DIR}/49-run0-cache.rules" /etc/polkit-1/rules.d/
}

gen_polkit_helper

echo "=== KROK 1: Czyszczenie starych plików budowy ==="
run_root rm -rf "${PROJECT_DIR}"
run_root rm -rf "${SCRIPT_DIR}/root"
run_root mkdir -p "${TARGET_BUILD_DIR}" "${LIVE_BUILD_DIR}" "${OVERLAY_IMG_DIR}"

echo "=== KROK 2: Budowanie profilu TargetRootfs (.squashfs) ==="
run_root kiwi-ng --profile=TargetRootfs system build \
    --description "." \
    --target-dir "${TARGET_BUILD_DIR}"

GENERATED_IMG=$(ls "${TARGET_BUILD_DIR}"/*.squashfs | head -n 1)

echo "=== KROK 3: Kopiowanie obrazu do struktury overlay ==="
echo "Kopiuję: ${GENERATED_IMG}"
echo "Do: ${OVERLAY_IMG_DIR}/system-rootfs.squashfs"

# Kopiujemy pod stałą nazwą, którą wcześniej wpisaliśmy do unpackfs.conf
run_root cp "${GENERATED_IMG}" "${OVERLAY_IMG_DIR}/system-rootfs.squashfs"

echo "=== KROK 4: Budowanie profilu LiveISO (.iso) ==="
run_root kiwi-ng --profile=Installer system build \
    --description "." \
    --target-dir "${LIVE_BUILD_DIR}"

echo "================================================="
echo "SUKCES! Twój instalacyjny obraz ISO znajduje się w:"
echo "${LIVE_BUILD_DIR}/"
echo "================================================="

