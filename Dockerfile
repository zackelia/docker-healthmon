FROM python:3.11-alpine3.18

RUN apk update && \
    apk add \
        docker \
        sudo && \
    adduser -D user && \
    echo "user ALL= NOPASSWD: $(python -c 'import site; print(site.getsitepackages()[0])')/healthmon/docker-events.sh" > /etc/sudoers.d/user-events-sh

COPY ./healthmon /healthmon
RUN python3 -m pip install /healthmon

COPY app.py /

# Immediately flush logs to docker logs.
ENV PYTHONUNBUFFERED=1

USER user
CMD ["/usr/local/bin/python3", "/app.py"]
