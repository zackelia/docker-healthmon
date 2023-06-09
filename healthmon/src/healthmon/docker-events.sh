#!/usr/bin/env sh

# Replace execution so that it can be SIGTERM'd easily by Python.
exec /usr/bin/docker events --filter event=health_status --format "{{json .}}"
