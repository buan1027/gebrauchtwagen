# syntax=docker.io/docker/dockerfile-upstream:1.22.0
# check=error=true

# Copyright (C) 2023 - present, Juergen Zimmermann, Hochschule Karlsruhe
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# Aufruf:   docker build --tag gebrauchtwagen:0.1.0 .
#           docker run --rm --publish 8000:8000 --env GEBRAUCHTWAGEN_DB_HOST=host.docker.internal gebrauchtwagen:0.1.0

ARG PYTHON_MAIN_VERSION=3.14
ARG PYTHON_VERSION=${PYTHON_MAIN_VERSION}.3
ARG UV_VERSION=0.10.11

# ------------------------------------------------------------------------------
# S t a g e   b u i l d e r
# ------------------------------------------------------------------------------
FROM ghcr.io/astral-sh/uv:${UV_VERSION}-python${PYTHON_MAIN_VERSION}-trixie-slim AS builder

WORKDIR /opt/app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv venv

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-default-groups --no-editable

COPY LICENSE README.md pyproject.toml uv.lock ./
COPY src ./src

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-default-groups --no-editable

# ------------------------------------------------------------------------------
# S t a g e   f i n a l
# ------------------------------------------------------------------------------
FROM python:${PYTHON_VERSION}-slim-trixie AS final

LABEL org.opencontainers.image.title="gebrauchtwagen" \
    org.opencontainers.image.description="Appserver fuer die Gebrauchtwagen-API" \
    org.opencontainers.image.version="0.1.0" \
    org.opencontainers.image.licenses="GPL-3.0-or-later"

WORKDIR /opt/app

RUN groupadd --gid 10000 app \
    && useradd --uid 10000 --gid app --shell /bin/bash --no-create-home app \
    && chown -R app:app /opt/app

USER app

COPY --from=builder --chown=app:app /opt/app ./

ENV PATH="/opt/app/.venv/bin:$PATH" \
    GEBRAUCHTWAGEN_SERVER_HOST=0.0.0.0 \
    GEBRAUCHTWAGEN_SERVER_PORT=8000 \
    GEBRAUCHTWAGEN_DB_HOST=db

EXPOSE 8000

STOPSIGNAL SIGINT

ENTRYPOINT ["python", "-m", "gebrauchtwagen"]
