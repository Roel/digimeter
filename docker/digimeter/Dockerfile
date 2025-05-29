FROM python:3.12-slim AS build

# Prevents Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid crashes without any logs
ENV PYTHONUNBUFFERED=1

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements-dev.txt,target=requirements-dev.txt \
    python -m pip install -r requirements-dev.txt

WORKDIR /app

# Copy the source code into the container.
COPY . .

RUN python install.py

FROM python:3.12-slim AS base

# Prevents Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid crashes without any logs
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/appuser" \
    --shell "/sbin/nologin" \
    --uid "${UID}" \
    appuser \
    && usermod -aG dialout appuser

# Update pip
RUN pip install --upgrade pip

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Copy the source code into the container.
COPY --from=build /app/lib/p1.py lib/p1.py
COPY --from=build /app/read_data.py .

# Switch to the non-privileged user to run the application.
USER appuser

# Run server
CMD python read_data.py