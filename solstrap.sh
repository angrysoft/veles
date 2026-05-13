#!/bin/sh

# Solstrap - A Solus Bootstrap Script

# Check if the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root. Please run with sudo."
    #exit 1
fi

out() { printf "$1 $2\n" "${@:3}"; }
error() { out "==> ERROR:" "$@"; } >&2
warning() { out "==> WARNING:" "$@"; } >&2
msg() { out "==>" "$@"; }
die() { error "$@"; exit 1; }

shopt -s extglob
REPO_SOLUS='https://cdn.getsol.us/repo/polaris/eopkg-index.xml.xz'
REPO_UNSTABLE='https://cdn.getsol.us/repo/unstable/eopkg-index.xml.xz'
repo="$REPO_SOLUS"
repo_name="Solus"
root="/sol"
bootloader=0
pkg="eopkg -y --destdir=$root"
nspawn="systemd-nspawn -D $root"



usage() {
    cat << EOF
usage: ${0##*/} [options] root [packages...]

  Options:
    -R <repo>  Choose a repository to use for installation. solus | unstable <Default is Solus> 
    -r <root>  Specify the root directory for the new system. <Default is /sol>
    -b         Install bootloader (CLR Boot Manager)
    -f         Generate fstab for the specified root directory and exit
EOF
}

check_command() {
    command -v "$1" >/dev/null 2>&1 || die "Required command not found: %s" "$1"
}

check_necessary_commands() {
    check_command "eopkg"
    # check_command "systemd-nspawn"
    if [[ $bootloader -eq 1 ]]; then
        check_command "clr-boot-manager"
    fi
    # Add any other necessary commands here
}

prepare_root() {
    msg "Preparing root directory: $root"
    if [[ -z "$root" ]]; then
        die "Root directory cannot be empty."
    fi

    if [[ -d "$root" ]]; then
        msg "Root directory already exists: $root"
    elif [[ -e "$root" ]];then
      die "root exist and is not a directory: $root"
    else
      msg "Creating root directory: $root"
      mkdir -p "$root" || die "Failed to create root directory: $root"
    fi
    mkdir -p "$root"/{dev/{pts,shm},run,tmp,proc} || die "Failed to create root directory: $root"
}

chroot_setup() {
  mount -t proc proc "$root/proc" || die "Failed to mount proc filesystem"
  mount -t sysfs sys "$root/sys" || die "Failed to mount sys filesystem"
  if [[ -d "/sys/firmware/efi/efivars" ]]; then
      mount -t efivarfs efivarfs "$root/sys/firmware/efi/efivars" || die "Failed to mount efivarfs"
  fi
  mount -t devtmpfs udev "$root/dev" || die "Failed to mount devtmpfs"
  mount -t devpts devpts "$root/dev/pts"  || die "Failed to mount devpts"
  mount -t tmpfs shm "$root/dev/shm"  || die "Failed to mount tmpfs for /dev/shm"
  mount /run "$root/run" --bind --make-private || die "Failed to mount /run"
  mount -t tmpfs tmp "$root/tmp" || die "Failed to mount tmpfs for /tmp"
}

umount_chroot() {
  umount -l "$root/proc" || warning "Failed to unmount proc filesystem"
  umount -l "$root/sys" || warning "Failed to unmount sys filesystem"
  if [[ -d "/sys/firmware/efi/efivars" ]]; then
      umount -l "$root/sys/firmware/efi/efivars" || warning "Failed to unmount efivarfs"
  fi
  umount -l "$root/dev/pts" || warning "Failed to unmount devpts"
  umount -l "$root/dev/shm" || warning "Failed to unmount tmpfs for /dev/shm"
  umount -l "$root/dev" || warning "Failed to unmount devtmpfs"
  umount -l "$root/run" || warning "Failed to unmount /run"
  umount -l "$root/tmp" || warning "Failed to unmount tmpfs for /tmp"
}


install_base_system() {
    msg "Installing base system using repository: $repo"
    $pkg add-repo "$repo_name" "$repo" || die "Failed to add repository: $repo"
    $pkg install -c system.base || die "Failed to install base system packages"
    $pkg install perl neovim btrfs-progs dosfstools  || die "Failed to install additional base packages"
    $pkg install network-manager || die "Failed to install NetworkManager"
    chroot_setup
    chroot "$root" usysconf run -f || die "Failed to install base system packages in chroot environment"
    #$nspawn usysconf run -f || die "Failed to install base system packages in nspawn environment"
    $pkg install linux-current linux-current-headers || die "Failed to install Linux kernel"
    umount_chroot
}

install_additional_packages() {
    if [[ ${#packages[@]} -gt 0 ]]; then
        msg "Installing additional packages: ${packages[*]}"
        $pkg install "${packages[@]}" || die "Failed to install additional packages: ${packages[*]}"
    fi
}

install_bootloader() {
    if [[ $bootloader -eq 1 ]]; then
        msg "Installing bootloader (CLR Boot Manager)"
        clr-boot-manager update --path "$root" || die "Failed to install bootloader"
    fi
}

gen_fstab() {
    msg "Generating fstab for $root"
    cp $root/usr/share/baselayout/fstab "$root/etc/fstab" || die "Failed to copy fstab"
    fs_whitelist="btrfs|ext4|ext3|ext2|vfat|ntfs|swap"

    while read -r src target fstype opts fsroot; do
        dump=0 pass=0
    
        if [[ $fstype =~ $fs_whitelist ]]; then
            uuid=$(lsblk -rno UUID "$src" 2>/dev/null)
            mount_point="${target//$root}"
            if [[ -z "$mount_point" ]]; then
                mount_point="/"
            fi

            if [[ "$fstype" == "btrfs" ]]; then
                opts=${opts//,subvolid=[0-9]/}
            elif [[ "$mount_point" == "/" ]]; then
                pass=1
            else
                pass=2
            fi
            echo "UUID=$uuid	$mount_point	$fstype	$opts	$dump	$pass" 
            echo "UUID=$uuid	$mount_point	$fstype	$opts	$dump	$pass" >> "$root/etc/fstab"
            # printf 'UUID=%s\t%-10s\t%s %s\n\n' "$uuid" "$mount_point" "$fstype" "$opts"  "$dump" "$pass" >> "$root/etc/fstab"
        else
            warning "Skipping unsupported filesystem type: $fstype for $src"
        fi

    done < <(findmnt -Recvruno SOURCE,TARGET,FSTYPE,OPTIONS,FSROOT "$root")
}



if [[ -z $1 || $1 = @(-h|--help) ]]; then
  usage
  exit $(( $# ? 0 : 1 ))
fi

while getopts ':R:r:bf' flag; do
  case $flag in
    R)
         repo=$OPTARG
         case $repo in
            solus)
              repo="$REPO_SOLUS"
              repo_name="Solus"
              ;;
            unstable)
              repo="$REPO_UNSTABLE"
              repo_name="Unstable"
              ;;
            *)
              die "Invalid repository specified: %s" "$repo"
              ;;
         esac
        ;;
    r)
        root="$OPTARG"
        ;;
    b)
        bootloader=1
        ;;
    f)
        gen_fstab
        exit 0
        ;;
    :)
      die '%s: option requires an argument -- '\''%s'\' "${0##*/}" "$OPTARG"
      ;;
    ?)
      die '%s: invalid option -- '\''%s'\' "${0##*/}" "$OPTARG"
      ;;
  esac
done

shift $(( OPTIND - 1 ))
packages=("$@")
check_necessary_commands
prepare_root
install_base_system
install_additional_packages
gen_fstab
install_bootloader

[[ -d $root ]] || die "%s is not a directory" "$root"


echo "Selected repository: ${repo:-Solus}"
