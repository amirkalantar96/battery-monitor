#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"
SERVICE_FILE="$HOME/.config/systemd/user/battery-monitor.service"

msg() { printf '\033[1;32m%s\033[0m\n' "$*"; }
warn() { printf '\033[1;33m%s\033[0m\n' "$*"; }

msg "Stopping and disabling service..."
systemctl --user disable --now battery-monitor.service 2>/dev/null || warn "Service was not enabled or already stopped."

msg "Removing service file..."
rm -f "$SERVICE_FILE"

msg "Reloading systemd user daemon..."
systemctl --user daemon-reload

if [ -d "$VENV_DIR" ]; then
  msg "Removing virtual environment..."
  rm -rf "$VENV_DIR"
fi

msg "Done."
