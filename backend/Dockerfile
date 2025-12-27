FROM python:3.11-slim

# Install system dependencies and uv
RUN apt-get update \
  && apt-get -y install tesseract-ocr curl \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Copy the rest of the application
COPY . /app

# Use shell form to allow environment variable substitution
CMD uv run uvicorn main:app --host=0.0.0.0 --port=${PORT:-8000}
