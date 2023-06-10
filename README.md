# docker-healthmon

[![Docker Image CI](https://github.com/zackelia/docker-healthmon/actions/workflows/docker-image.yml/badge.svg)](https://github.com/zackelia/docker-healthmon/actions/workflows/docker-image.yml)

> Automatic docker health check monitoring and reporting

# About

`healthmon` is a Docker image that monitors all containers on the running system that report health checks. Upon a change, it sends a notification using [Apprise](https://github.com/caronc/apprise).

# Usage

`healthmon` can be run simply with a docker-compose.yml file.

```yml
services:
  healthmon:
    image: ghcr.io/zackelia/healthmon:latest
    container_name: healthmon
    restart: unless-stopped
    hostname: my-server
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
        # Find all supported URLs at: https://github.com/caronc/apprise
      - APPRISE_URL=mailto://userid:pass@domain.com
```

## Advanced

For services not supported by Apprise, you can create `custom/hooks.py` and mount it at `./custom:/custom`. The content of this file can be created using Apprise's [Custom Notifications](https://github.com/caronc/apprise/wiki/decorator_notify) page. On container start, `healthmon` will log that it loaded the custom hooks.

# Security

`healthmon` requires mounting in `/var/run/docker.sock` which is inherently dangerous as it allows [trivial access to root on the host](https://gtfobins.github.io/gtfobins/docker/).

To remedy this, `healthmon` creates a non-privileged user that is only allowed to run a specific `docker events` command to subscribe to health status messages. No other elevated permissions are granted.
