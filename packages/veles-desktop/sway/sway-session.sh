#!/bin/sh
export XDG_CURRENT_DESKTOP=sway
export XDG_SESSION_DESKTOP="${XDG_SESSION_DESKTOP:-sway}"
export XDG_SESSION_TYPE=wayland
export QT_QPA_PLATFORM=wayland
export QT_QPA_PLATFORMTHEME=gtk3
export QT_QUICK_CONTROLS_STYLE=Basic
export QT_LOGGING_RULES="qt.qpa.services=false"
VARIABLES="DESKTOP_SESSION XDG_CURRENT_DESKTOP XDG_SESSION_DESKTOP XDG_SESSION_TYPE GNOME_KEYRING_CONTROL"
VARIABLES="${VARIABLES} DISPLAY I3SOCK SWAYSOCK WAYLAND_DISPLAY"
VARIABLES="${VARIABLES} XCURSOR_THEME XCURSOR_SIZE SSH_AUTH_SOCK"
VARIABLES="${VARIABLES} QT_QPA_PLATFORM QT_QPA_PLATFORMTHEME QT_LOGGING_RULES QT_QUICK_CONTROLS_STYLE"
SESSION_TARGET="sway-session.target"
SESSION_SHUTDOWN_TARGET="sway-session-shutdown.target"


# Check if another Sway session is already active.
#
# Ignores all other kinds of parallel or nested sessions
# (Sway on Gnome/KDE/X11/etc.), as the only way to detect these is to check
# for (WAYLAND_)?DISPLAY and that is know to be broken on Arch.
if systemctl --user -q is-active "$SESSION_TARGET"; then
    echo "Another session found; refusing to overwrite the variables"
    exit 1
fi

# DBus activation environment is independent from systemd. While most of
# dbus-activated services are already using `SystemdService` directive, some
# still don't and thus we should set the dbus environment with a separate
# command.
if hash dbus-update-activation-environment 2>/dev/null; then
    # shellcheck disable=SC2086
    dbus-update-activation-environment --systemd ${VARIABLES:- --all}
fi

# reset failed state of all user units
systemctl --user reset-failed

# shellcheck disable=SC2086
systemctl --user import-environment $VARIABLES
systemctl --user start "$SESSION_TARGET"

# Optionally, wait until the compositor exits and cleanup variables and services.
if [ -z "$WITH_CLEANUP" ] ||
    [ -z "$SWAYSOCK" ] ||
    ! hash swaymsg 2>/dev/null
then
    exit 0;
fi

# declare cleanup handler and run it on script termination via kill or Ctrl-C
session_cleanup () {
    # stop the session target and unset the variables
    systemctl --user start --job-mode=replace-irreversibly "$SESSION_SHUTDOWN_TARGET"
    if [ -n "$VARIABLES" ]; then
        # shellcheck disable=SC2086
        systemctl --user unset-environment $VARIABLES
    fi
}
trap session_cleanup INT TERM
# wait until the compositor exits
swaymsg -t subscribe '["shutdown"]'
# run cleanup handler on normal exit
session_cleanup

