# Battery Monitor

A simple Python-based battery monitoring tool designed to help maintain laptop battery health by keeping the charge level between **30% and 80%**. It sends desktop notifications to remind you when it’s time to plug in or unplug your charger.

> ⚠️ **Note:** This project is currently in early development and tailored for **Ubuntu Desktop** environments. More features will be added over time.

---

## 🎯 Purpose

Laptop batteries degrade faster when frequently charged to 100% or drained below 20%. This utility helps users maintain optimal charging habits by:

- Notifying when the battery drops to **30%**, suggesting it’s time to plug in.
- Notifying when the battery reaches **80% while plugged in**, suggesting it’s safe to unplug.

This way, you don’t have to worry about manually checking your battery level anymore!

---

## 🔧 Features

- Monitors battery percentage and power source status.
- Sends desktop notifications using `notify-send`.
- Prevents repeated alerts using state tracking.
- Lightweight and easy to run in the background.
- Supports installation as a systemd `--user` service.
- Uses a local Python virtualenv for isolated dependencies.
- Can be installed and removed with helper scripts.

---

## 📦 Requirements

- **Operating System**: Ubuntu Desktop (Tested on 24.04 LTS)
- **Language**: Python 3.x
- **Dependencies**:
  - `psutil` — for accessing system and battery information
  - `libnotify-bin` — provides the `notify-send` command

### Install system packages

```bash
sudo apt update
sudo apt install python3-venv libnotify-bin
```

`psutil` is installed inside the project virtual environment.

---

## ▶️ How to Run

The monitor can be run manually for testing, or installed as a systemd `--user` service so it starts automatically after login.

### Manual run

1. Clone the repository and navigate to the project directory:

```bash
git clone <repository-url>
cd <project-directory>
```

2. Create a Python virtual environment:

```bash
python3 -m venv .venv
```

3. Activate the virtual environment:

```bash
source .venv/bin/activate
```

4. Install the required Python dependency:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

5. Run the battery monitor:

```bash
python monitor.py
```

### Recommended installation

To run the monitor automatically after login, use the install script:

```bash
chmod +x install.sh uninstall.sh
./install.sh
```

This will:

- create `.venv`
- install Python dependencies
- generate the systemd `--user` service file in `~/.config/systemd/user/`
- enable and start the service

Once enabled, the service is picked up by your per-user systemd instance and starts automatically each time you log in.

---

## ⚙️ Service management

If the service is installed, you can control it with:

```bash
systemctl --user status battery-monitor.service
systemctl --user start battery-monitor.service
systemctl --user stop battery-monitor.service
systemctl --user restart battery-monitor.service
systemctl --user enable battery-monitor.service
systemctl --user disable battery-monitor.service
```

To reload user services after changes to the service file:

```bash
systemctl --user daemon-reload
```

To view the service logs:

```bash
journalctl --user -u battery-monitor.service
```

---

## 🧹 Uninstall

To remove the service and the local virtual environment:

```bash
./uninstall.sh
```

This stops and disables the service, removes the generated service file from `~/.config/systemd/user/`, and deletes `.venv`.

---

## 🛠 Future Improvements

- ☐ Add configuration file support (e.g., custom thresholds).
- ☐ Package as a system tray application.
- ☐ Support for other Linux distributions.
- ☐ GUI version using PyQt or Tkinter.

---

## 📄 License

This project is open-source and available under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). Feel free to fork, modify, and distribute.

---

## 💬 Feedback & Contributions

Contributions are welcome! If you encounter bugs or would like to suggest improvements, please open an issue or submit a pull request.
