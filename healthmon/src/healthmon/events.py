import dataclasses
import json
import shutil
import subprocess
from typing import Generator


@dataclasses.dataclass
class HealthStatusEvent:
    """A health-status event from Docker."""

    healthy: bool
    container_name: str

    def __init__(self, healthy: bool, container_name: str):
        self.healthy = healthy
        self.container_name = container_name


def docker_health_status_events() -> Generator[HealthStatusEvent, None, None]:
    """Parse health-status events from the Docker client."""
    docker = shutil.which("docker")
    assert docker

    process = subprocess.Popen(
        [
            docker,
            "events",
            "--filter",
            "event=health_status",
            "--format",
            "{{json .}}",
        ],
        stdout=subprocess.PIPE,
    )
    assert process.stdout

    for line in iter(process.stdout.readline, b""):
        data = json.loads(line.decode().strip())
        healthy = True if data["status"].split(" ")[-1] == "healthy" else False
        container_name = data["Actor"]["Attributes"]["name"]

        yield HealthStatusEvent(healthy, container_name)
