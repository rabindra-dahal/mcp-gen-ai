FROM python:3.11-slim

WORKDIR /workspace
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app

EXPOSE 8000

# Run using the streamable-http protocol standard over an enterprise Uvicorn engine
CMD ["uvicorn", "app.main:mcp.asgi", "--host", "0.0.0.0", "--port", "8000"]
