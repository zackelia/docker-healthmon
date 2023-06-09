import dataclasses
import json
import signal
import subprocess
from typing import Any, Generator

import pkg_resources

process: subprocess.Popen | None = None


@dataclasses.dataclass
class HealthStatusEvent:
    """A health-status event from Docker."""

    healthy: bool
    container_name: str

    def __init__(self, healthy: bool, container_name: str):
        self.healthy = healthy
        self.container_name = container_name


def _terminate_docker_events(*_: Any) -> None:
    global process
    assert process
    # Docker will fail to stop child processes sending SIGTERM to this module alone.
    process.terminate()


def docker_health_status_events() -> Generator[HealthStatusEvent, None, None]:
    """Parse health-status events from the Docker client."""
    signal.signal(signal.SIGTERM, _terminate_docker_events)

    events_script = pkg_resources.resource_filename("healthmon", "docker-events.sh")

    global process
    process = subprocess.Popen(
        [
            "sudo",
            events_script,
        ],
        stdout=subprocess.PIPE,
    )
    assert process.stdout

    for line in iter(process.stdout.readline, b""):
        data = json.loads(line.decode().strip())
        healthy = True if data["status"].split(" ")[-1] == "healthy" else False
        container_name = data["Actor"]["Attributes"]["name"]

        yield HealthStatusEvent(healthy, container_name)
