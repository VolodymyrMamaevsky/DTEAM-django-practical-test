FROM python:3.12-slim AS base

ARG USER_ID=1000
ARG GROUP_ID=1000
ARG NONROOT_USER=nonroot
ARG PYSETUP_PATH=/opt/pysetup

ENV PATH="${PYSETUP_PATH}/.venv/bin:${PATH}"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENV=local

RUN groupadd --gid ${GROUP_ID} ${NONROOT_USER} && \
    useradd --uid ${USER_ID} --gid ${GROUP_ID} --create-home --home-dir ${PYSETUP_PATH} ${NONROOT_USER} && \
    mkdir -p ${PYSETUP_PATH}/app && \
    chown -R ${NONROOT_USER}:${NONROOT_USER} ${PYSETUP_PATH}

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    # WeasyPrint dependencies
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry

USER ${NONROOT_USER}
WORKDIR ${PYSETUP_PATH}

COPY --chown=${NONROOT_USER}:${NONROOT_USER} pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create true && \
    poetry config virtualenvs.in-project true && \
    poetry install --no-root

FROM base AS runtime

COPY --from=base ${PYSETUP_PATH}/.venv ${PYSETUP_PATH}/.venv
COPY --chown=${NONROOT_USER}:${NONROOT_USER} . ${PYSETUP_PATH}/app

WORKDIR ${PYSETUP_PATH}/app

# Make entrypoint script executable
RUN chmod +x entrypoint.sh

# Install WeasyPrint
USER root
RUN pip install weasyprint
USER ${NONROOT_USER}

ENTRYPOINT ["/opt/pysetup/app/entrypoint.sh"]
