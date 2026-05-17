#!/bin/bash
systemctl set-default multi-user.target

# systemctl enable getty@tty1.service
systemctl enable NetworkManager.service

# mkdir -p /etc/systemd/system/getty@tty1.service.d

# cat <<EOF > /etc/systemd/system/getty@tty1.service.d/override.conf
# [Service]
# ExecStart=
# ExecStart=-/sbin/agetty --autologin live --noclear %I $TERM
# EOF

# systemctl daemon-reload
# systemctl enable getty@tty1.service

# cat <<EOF > /home/live/.bash_profile
# if [ -z "$DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then
#     # Zmienne środowiskowe dla Qt/Wayland
#     export QT_QPA_PLATFORM=wayland
#     export XDG_RUNTIME_DIR=/run/user/0
    
#     mkdir -p $XDG_RUNTIME_DIR
#     chmod 700 $XDG_RUNTIME_DIR

#     exec cage -- calamares -d
# fi
# EOF

cat <<EOF > /etc/systemd/system/calamares-installer.service
[Unit]
Description=Calamares Installer Kiosk Mode (Weston)
After=systemd-user-sessions.service plymouth-quit-wait.service systemd-udevd.service
Before=getty@tty1.service
Conflicts=getty@tty1.service

[Service]
Type=simple
User=root
WorkingDirectory=/root

# Wymagane zmienne dla środowiska Wayland i Qt
Environment=XDG_RUNTIME_DIR=/run/user/0
Environment=WAYLAND_DISPLAY=wayland-0
Environment=QT_QPA_PLATFORM=wayland

ExecStartPre=/usr/bin/mkdir -p /run/user/0
ExecStartPre=/usr/bin/chmod 0700 /run/user/0

ExecStart=/usr/bin/weston --tty=1 --config=/etc/xdg/weston/weston.ini

Restart=on-failure
StandardInput=tty-fail
StandardOutput=journal

[Install]
WantedBy=multi-user.target
EOF


mkdir -p /etc/xdg/weston
cat <<EOF > /etc/xdg/weston/weston.ini
[core]
shell=kiosk-shell.so
backend=drm-backend.so

[autostart]
path=/usr/bin/calamares
EOF


systemctl disable getty@tty1.service
systemctl enable calamares-installer.service
# systemctl enable polkit.service
exit 1