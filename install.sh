#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"
SERVICE_DIR="$HOME/.config/systemd/user"
SERVICE_FILE="$SERVICE_DIR/battery-monitor.service"
TEMPLATE_FILE="$PROJECT_DIR/systemd/battery-monitor.service.tpl"

msg() { printf '\033[1;32m%s\033[0m\n' "$*"; }
warn() { printf '\033[1;33m%s\033[0m\n' "$*"; }
die() { printf '\033[1;31m%s\033[0m\n' "$*" >&2; exit 1; }

command -v python3 >/dev/null 2>&1 || die "python3 is not installed."
[ -f "$TEMPLATE_FILE" ] || die "Missing template file: $TEMPLATE_FILE"
[ -f "$PROJECT_DIR/requirements.txt" ] || die "Missing requirements.txt"

msg "[1/4] Creating virtual environment..."
if [ -d "$VENV_DIR" ]; then
  warn "Virtual environment already exists: $VENV_DIR"
else
  python3 -m venv "$VENV_DIR"
fi

msg "[2/4] Installing Python dependencies..."
"$VENV_DIR/bin/python" -m pip install --upgrade pip
"$VENV_DIR/bin/python" -m pip install -r "$PROJECT_DIR/requirements.txt"

msg "[3/4] Generating systemd user service..."
mkdir -p "$SERVICE_DIR"
tmp_service="$(mktemp)"
trap 'rm -f "$tmp_service"' EXIT

sed \
  -e "s|__PROJECT_DIR__|$PROJECT_DIR|g" \
  -e "s|__VENV_PYTHON__|$VENV_DIR/bin/python|g" \
  "$TEMPLATE_FILE" > "$tmp_service"

install -m 0644 "$tmp_service" "$SERVICE_FILE"

msg "[4/4] Reloading systemd user daemon and enabling service..."
systemctl --user daemon-reload
systemctl --user enable --now battery-monitor.service

msg "Done."
msg "Service installed: $SERVICE_FILE"
msg "Venv created: $VENV_DIR"
