# Use this image for Z2JH where the singleuser server static-redirector and
# desktop containers are seperate
#
# docker.io/manics/jupyter-static-redirector
FROM docker.io/library/python:3.13.0-slim-bookworm

RUN useradd --create-home --uid 1000 jovyan

COPY static_redirector /src/static_redirector
COPY etc /src/etc
COPY pyproject.toml README.md requirements.txt /src/
RUN pip install --no-cache-dir \
    -r /src/requirements.txt \
    /src/

COPY jupyter_server_config.py /etc/jupyter/

USER jovyan
EXPOSE 8888
CMD ["jupyterhub-singleuser"]
