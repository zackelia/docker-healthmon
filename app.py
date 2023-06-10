try:
    # Allow for custom apprise hooks
    import custom.hooks

    print("Loaded custom apprise hook")
except:
    pass

from healthmon.events import docker_health_status_events
from healthmon.notifications import notify

print("Monitoring containers...")

for event in docker_health_status_events():
    notify(event)
