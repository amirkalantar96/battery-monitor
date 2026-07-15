#!/usr/bin/env python3
"""
Battery Monitor - monitors battery level and sends desktop notifications
at 30% (low) and 80% (full enough to unplug)
"""

import time
import subprocess
import psutil

# Thresholds
LOW_BATTERY = 30
HIGH_BATTERY = 80

# Check interval in seconds
CHECK_INTERVAL = 60


def send_notification(title: str, message: str, urgency: str = "normal") -> None:
    """Send a desktop notification using notify-send."""
    subprocess.run(
        ["notify-send", "-u", urgency, title, message],
        check=False
    )


def get_battery() -> psutil.sensors_battery:
    """Return battery status or None if no battery found."""
    return psutil.sensors_battery()


def monitor_battery() -> None:
    """Main loop: check battery every CHECK_INTERVAL seconds."""
    notified_low = False
    notified_high = False

    print("Battery monitor started...")

    while True:
        battery = get_battery()

        if battery is None:
            print("No battery detected. Exiting.")
            break

        percent = battery.percent
        plugged = battery.power_plugged

        print(f"Battery: {percent:.1f}% | Plugged: {plugged}")

        # Low battery warning - notify when unplugged and below threshold
        if percent <= LOW_BATTERY and not plugged and not notified_low:
            send_notification(
                "⚠️ باتری کم است",
                f"شارژ باتری به {percent:.0f}٪ رسیده. لطفاً شارژر را وصل کنید.",
                urgency="critical"
            )
            notified_low = True

        # Reset low notification when plugged in
        if plugged and notified_low:
            notified_low = False

        # High battery warning - notify when plugged and above threshold
        if percent >= HIGH_BATTERY and plugged and not notified_high:
            send_notification(
                "🔋 شارژ کافی است",
                f"شارژ باتری به {percent:.0f}٪ رسیده. می‌توانید شارژر را جدا کنید.",
                urgency="normal"
            )
            notified_high = True

        # Reset high notification when unplugged
        if not plugged and notified_high:
            notified_high = False

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    monitor_battery()
