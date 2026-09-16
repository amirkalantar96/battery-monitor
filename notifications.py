import subprocess

def send_notification(title: str, message: str, urgency: str = "normal") -> None:
    """Send a desktop notification using notify-send."""
    subprocess.run(
        ["notify-send", "-u", urgency, title, message],
        check=False
    )
