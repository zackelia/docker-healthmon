import datetime
import os
import socket
import sys
from typing import Any

import apprise

from .events import HealthStatusEvent

if "APPRISE_URL" not in os.environ:
    print("Could not get APPRISE_URL from environment, exiting")
    sys.exit(1)

app = apprise.Apprise()
app.add(os.environ["APPRISE_URL"])


def notify(event: HealthStatusEvent) -> None:
    """Send a notification to APPRISE_URL."""

    if event.healthy:
        status = f"😊 healthy"
        notify_type = apprise.NotifyType.INFO
    else:
        status = f"🤒 unhealthy"
        notify_type = apprise.NotifyType.WARNING

    title = socket.gethostname()
    body = f"{event.container_name} ({status})"
    now = datetime.datetime.now()

    print(f"{now} - {title} - {body}")

    result = app.notify(title=title, body=body, notify_type=notify_type)
    if not result:
        # It would be nice to mark the container unhealthy here but then we
        # would need a healthmon for healthmon...
        print(f"Could not send notification to {app.urls()}")
