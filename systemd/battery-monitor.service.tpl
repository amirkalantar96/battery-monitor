[Unit]
Description=Battery Monitor
After=default.target

[Service]
Type=simple
ExecStart=__VENV_PYTHON__ __PROJECT_DIR__/monitor.py
WorkingDirectory=__PROJECT_DIR__
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
