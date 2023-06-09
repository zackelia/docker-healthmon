from healthmon.events import docker_health_status_events

for event in docker_health_status_events():
    print(event)
