#!/bin/bash
if [ "$EUID" -ne 0 ]; then
    echo "run script with sudo"
    exit 1
fi
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SERVICE_USER="${SUDO_USER:-$USER}"
SERVICE_FILE="/etc/systemd/system/server-health-checker.service"
    REQUIRED_FILES=(
    "$PROJECT_DIR/server_health_checker.py"
    "$PROJECT_DIR/config/config.yaml"
    "$PROJECT_DIR/systemd/server-health-checker.service.example"
    )
    for file in "${REQUIRED_FILES[@]}"; do
        if [ ! -f "$file" ]; then
            echo "ERROR: required file not found: $file"
            exit 1
        fi
            done
    sed \
    -e "s/__SERVICE_USER__/$SERVICE_USER/" \
    -e "s|__PROJECT_DIR__|$PROJECT_DIR|g" \
    "$PROJECT_DIR/systemd/server-health-checker.service.example" \
    > "$SERVICE_FILE"

    systemctl daemon-reload
    systemctl enable server-health-checker.service
    systemctl start server-health-checker.service
    if systemctl is-active --quiet server-health-checker.service; then
        echo "SUCCESS"
    else
        echo "ERROR: service failed to start"
        systemctl status server-health-checker.service --no-pager
        exit 1
    fi