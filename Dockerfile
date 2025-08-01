FROM ubuntu:25.04

# Set environment vars
ENV DEBIAN_FRONTEND=noninteractive \
    PYENV_ROOT="/root/.pyenv" \
    PATH="/root/.pyenv/bin:/root/.pyenv/shims:$PATH"

# --- 1. Install system dependencies ---
RUN apt-get update && apt-get install -y \
    make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
    git python3-pip && \
    apt-get clean

# --- 2. Install pyenv ---
RUN curl https://pyenv.run | bash && \
    echo 'eval "$(pyenv init --path)"' >> /etc/profile.d/pyenv.sh

# --- 3. Install all Python versions (cached layer) ---
RUN bash -c '\
    export PYENV_ROOT="/root/.pyenv"; \
    export PATH="$PYENV_ROOT/bin:$PATH"; \
    eval "$(pyenv init -)"; \
    for version in 3.{6..13}; do pyenv install -s $version; done; \
    pyenv global 3.12'

# --- 4. Install pip tools and Python project dependencies (cached separately) ---

COPY poetry.lock pyproject.toml /app/
WORKDIR /app

# Install poetry and deps in ALL pyenv Python versions
RUN bash -c '\
    export PYENV_ROOT="/root/.pyenv"; \
    export PATH="$PYENV_ROOT/bin:$PATH"; \
    eval "$(pyenv init -)"; \
    pip install --upgrade pip; \
    pip install poetry; \
    poetry config virtualenvs.create false; \
    poetry install --no-root'

# --- 5. Copy the rest of the project ---
COPY . /app/

# --- 6. Default command to run tests using cflow.py ---
CMD bash -c '\
    poetry install; \
    eval "$(pyenv init -)"; \
    pyenv global 3.12; \
    echo '' > test_output.jsonl; \
    for version in 3.{6..13}; do \
        for file in test/*.py; do \
            python dev_scripts/cflow.py "$file" -v "$version" -j >> test_output.jsonl; \
        done; \
    done; \
    python testreport.py;'

