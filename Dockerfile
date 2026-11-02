# Runtime for the ds runner. The repo itself is NOT baked in: it is mounted at
# /app, because runs edit content/ and commit, and those commits belong in the
# checkout on the host, not in a container layer that disappears.
#
# Node is the base because the website repo needs it (npm run validate runs
# inside the blog stage). Python comes from uv; the Claude CLI comes bundled
# with claude-agent-sdk.
FROM node:22-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        chromium imagemagick git jq perl openssh-client ca-certificates tzdata \
    && rm -rf /var/lib/apt/lists/* \
    # Mounted repos are owned by the host user; without this git refuses them.
    && git config --system safe.directory '*'

COPY --from=ghcr.io/astral-sh/uv:0.13.6 /uv /usr/local/bin/uv
ENV UV_PYTHON_INSTALL_DIR=/opt/python \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv python install 3.12 \
    && uv sync --frozen --no-dev --no-install-project \
    && ln -s "$(/opt/venv/bin/python -c 'import claude_agent_sdk, pathlib; print(pathlib.Path(claude_agent_sdk.__file__).parent / "_bundled" / "claude")')" /usr/local/bin/claude \
    && printf '#!/bin/sh\nexec /opt/venv/bin/python -m ds "$@"\n' > /usr/local/bin/ds \
    && chmod +x /usr/local/bin/ds

# Match the host user that owns the checkouts, so files the runs write stay
# editable on the host. Build with --build-arg UID=$(id -u).
ARG UID=1000
RUN if [ "$UID" != "1000" ]; then usermod -u "$UID" node; fi \
    && mkdir -p /home/node/.claude && chown node /home/node/.claude

ENV PATH=/opt/venv/bin:$PATH \
    TZ=America/Panama \
    PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    CHROME_BIN=chromium \
    CHROME_NO_SANDBOX=1 \
    CLAUDE_CONFIG_DIR=/home/node/.claude \
    WEBSITE_REPO=/work/website

USER node
ENTRYPOINT ["ds"]
CMD ["--help"]
