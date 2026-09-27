#!/bin/bash
if [ "$EUID" -ne 0 ]; then
    echo "run script with sudo"
    exit 1
fi
SERVICE_NAME="server-health-checker.service"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME"
    systemctl stop "$SERVICE_NAME"
    systemctl disable "$SERVICE_NAME"
    rm "$SERVICE_FILE"
    systemctl daemon-reload
    echo "SUCCESS"