#!/usr/bin/env python3
"""
Battery Monitor - monitors battery level and sends desktop notifications
at 30% (low) and 80% (full enough to unplug)
Repeats notifications every REMINDER_INTERVAL seconds if condition persists.
"""

import time
from config import LOW_BATTERY, HIGH_BATTERY, CHECK_INTERVAL, REMINDER_INTERVAL
from notifications import send_notification
from battery import get_battery_status

class BatteryMonitor:
    def __init__(self):
        self.last_notified_low = 0.0
        self.last_notified_high = 0.0

    def run(self):
        print("Battery monitor started...")
        while True:
            battery = get_battery_status()

            if battery is None:
                print("No battery detected. Exiting.")
                break

            percent = battery.percent
            plugged = battery.power_plugged
            now = time.monotonic()

            print(f"Battery: {percent:.1f}% | Plugged: {plugged}")

            # Low battery warning
            if percent <= LOW_BATTERY and not plugged:
                if now - self.last_notified_low >= REMINDER_INTERVAL:
                    send_notification(
                        "⚠️ Battery Low",
                        f"Battery charge has reached {percent:.0f}%. Please plug in the charger.",
                        urgency="critical"
                    )
                    self.last_notified_low = now
            else:
                self.last_notified_low = 0.0

            # High battery warning
            if percent >= HIGH_BATTERY and plugged:
                if now - self.last_notified_high >= REMINDER_INTERVAL:
                    send_notification(
                        "🔋 Battery Sufficient",
                        f"Battery charge has reached {percent:.0f}%. You can unplug the charger.",
                        urgency="normal"
                    )
                    self.last_notified_high = now
            else:
                self.last_notified_high = 0.0

            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    BatteryMonitor().run()
