#!/bin/bash
systemctl set-default multi-user.target

systemctl enable getty@tty1.service
systemctl enable NetworkManager.service

exit 0