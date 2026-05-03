# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies for binary packages (Avro/Pandas)
RUN apt-get update && apt-get install -y \
    build-essential \
    liblzma-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim as runtime

WORKDIR /app
RUN useradd -m parseruser
USER parseruser

# Copy installed packages from builder
COPY --from=builder /root/.local /home/parseruser/.local
COPY . .

# Update PATH for the non-root user
ENV PATH=/home/parseruser/.local/bin:$PATH

# Default command runs the parser tests to verify the environment
CMD ["pytest", "tests/"]