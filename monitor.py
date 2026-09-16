#!/usr/bin/env python3
"""
Battery Monitor - monitors battery level and sends desktop notifications
at 30% (low) and 80% (full enough to unplug)
Repeats notifications every REMINDER_INTERVAL seconds if condition persists.
"""

import time
import subprocess
import psutil

# Thresholds
LOW_BATTERY = 30
HIGH_BATTERY = 80

# Check interval in seconds
CHECK_INTERVAL = 60

# Reminder interval in seconds (re-notify if condition still active)
REMINDER_INTERVAL = 60


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
    last_notified_low: float = 0.0
    last_notified_high: float = 0.0

    print("Battery monitor started...")

    while True:
        battery = get_battery()

        if battery is None:
            print("No battery detected. Exiting.")
            break

        percent = battery.percent
        plugged = battery.power_plugged
        now = time.monotonic()

        print(f"Battery: {percent:.1f}% | Plugged: {plugged}")

        # Low battery warning - notify when unplugged and below threshold
        if percent <= LOW_BATTERY and not plugged:
            if now - last_notified_low >= REMINDER_INTERVAL:
                send_notification(
                    "⚠️ Battery Low",
                    f"Battery charge has reached {percent:.0f}%. Please plug in the charger.",
                    urgency="critical"
                )
                last_notified_low = now
        else:
            # Reset so it fires immediately if condition returns
            last_notified_low = 0.0

        # High battery warning - notify when plugged and above threshold
        if percent >= HIGH_BATTERY and plugged:
            if now - last_notified_high >= REMINDER_INTERVAL:
                send_notification(
                    "🔋 Battery Sufficient",
                    f"Battery charge has reached {percent:.0f}%. You can unplug the charger.",
                    urgency="normal"
                )
                last_notified_high = now
        else:
            # Reset so it fires immediately if condition returns
            last_notified_high = 0.0

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    monitor_battery()
