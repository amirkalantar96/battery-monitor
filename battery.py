import psutil

def get_battery_status():
    """Return battery status or None if no battery found."""
    return psutil.sensors_battery()
