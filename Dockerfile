FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml README.md mcp_applemusic.py ./

RUN pip install --no-cache-dir .

ENTRYPOINT ["mcp-applemusic"]
