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
Description=Calamares Live Installer
After=systemd-user-sessions.service plymouth-quit-wait.service gettys.target
Conflicts=getty@tty1.service

[Service]
Type=simple
User=root
WorkingDirectory=/root
Environment=XDG_RUNTIME_DIR=/run/user/0
Environment=QT_QPA_PLATFORM=wayland-egl
ExecStartPre=/usr/bin/mkdir -p /run/user/0
ExecStartPre=/usr/bin/chmod 700 /run/user/0
ExecStart=/usr/bin/cage -- /usr/bin/calamares -d
StandardOutput=tty
StandardError=tty
TTYPath=/dev/tty1

[Install]
WantedBy=graphical.target
EOF


systemctl disable getty@tty1.service
systemctl enable calamares-installer.service
systemctl enable polkit.service
exit 1