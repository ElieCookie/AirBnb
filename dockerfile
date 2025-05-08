FROM mcr.microsoft.com/playwright/python:v1.52.0-jammy

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

# Run tests but prevent container from exiting on failure, then keep alive
CMD ["/bin/sh", "-c", "pytest tests -o log_cli=true -o log_cli_level=INFO || true && tail -f /dev/null"]
