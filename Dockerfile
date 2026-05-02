# Stage 1: Builder/Test
FROM python:3.9-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pytest tests/ && flake8 extension/

# Stage 2: Production Runtime
FROM python:3.9-slim as runtime
WORKDIR /app
RUN useradd -m parseruser
USER parseruser
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /app/extension ./extension
EXPOSE 8000
CMD ["python", "extension/main.py"]

# Stage 3: Development
FROM builder as dev
RUN pip install pytest-watch
CMD ["ptw", "--", "tests/", "--cov=extension"]