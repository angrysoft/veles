#!/bin/sh
set -e

mkdir -p $(pwd)/root/usr/share/veles-images

PROJECT_DIR="$(pwd)/tmp"
TARGET_BUILD_DIR="${PROJECT_DIR}/build/target"
LIVE_BUILD_DIR="${PROJECT_DIR}/build/live"
OVERLAY_IMG_DIR="${PROJECT_DIR}/root/usr/share/veles-images"

echo "=== KROK 1: Czyszczenie starych plików budowy ==="
sudo rm -rf "${PROJECT_DIR}/build"
mkdir -p "${TARGET_BUILD_DIR}" "${LIVE_BUILD_DIR}" "${OVERLAY_IMG_DIR}"

echo "=== KROK 2: Budowanie profilu TargetRootfs (.img) ==="
sudo kiwi-ng --profile=TargetRootfs system build \
    --description "${PROJECT_DIR}" \
    --target-dir "${TARGET_BUILD_DIR}"

GENERATED_IMG=$(ls "${TARGET_BUILD_DIR}"/*.img | head -n 1)

echo "=== KROK 3: Kopiowanie obrazu do struktury overlay ==="
echo "Kopiuję: ${GENERATED_IMG}"
echo "Do: ${OVERLAY_IMG_DIR}/system-rootfs.img"

# Kopiujemy pod stałą nazwą, którą wcześniej wpisaliśmy do unpackfs.conf
sudo cp "${GENERATED_IMG}" "${OVERLAY_IMG_DIR}/system-rootfs.img"

echo "=== KROK 4: Budowanie profilu LiveISO (.iso) ==="
sudo kiwi-ng --profile=LiveISO system build \
    --description "${PROJECT_DIR}" \
    --target-dir "${LIVE_BUILD_DIR}"

echo "================================================="
echo "SUKCES! Twój instalacyjny obraz ISO znajduje się w:"
echo "${LIVE_BUILD_DIR}/"
echo "================================================="

