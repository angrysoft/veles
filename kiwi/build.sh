#!/bin/sh
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

PROJECT_DIR="${SCRIPT_DIR}/tmp"
LIVE_BUILD_DIR="${PROJECT_DIR}/build/live"
OVERLAY_IMG_DIR="${SCRIPT_DIR}/root/usr/share/veles-images"
RM="rm -rf"
MKDIR="mkdir -pv"
CP="cp -v"


check_root() {
    if [ "$(id -u)" -ne 0 ]; then
        echo "Ten skrypt musi być uruchomiony jako root lub za pomocą run0."
        exit 1
    fi
}

check_root

echo "=== KROK 1: Czyszczenie starych plików budowy ==="
$RM "${PROJECT_DIR}"
$RM "${SCRIPT_DIR}/root"
$MKDIR "${LIVE_BUILD_DIR}" "${OVERLAY_IMG_DIR}"

echo "=== KROK 2: Budowanie obrazu systemu docelowego ==="
kiwi-ng --type iso system build \
    --description "." \
    --target-dir "${LIVE_BUILD_DIR}"


echo "================================================="
echo "SUKCES! Twój instalacyjny obraz ISO znajduje się w:"
echo "${LIVE_BUILD_DIR}/"
echo "================================================="
