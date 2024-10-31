FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

# Keeps Python from generating .pyc files in the container 
ENV PYTHONDONTWRITEBYTECODE=1 
 
# Turns off buffering for easier container logging 
ENV PYTHONUNBUFFERED=1 

# Package mananger uv
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:0.4.20 /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
