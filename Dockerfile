FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

LABEL org.opencontainers.image.source="https://github.com/houcem58/ConversaETL-Showcase"
LABEL org.opencontainers.image.description="ConversaETL — Natural language to ETL pipeline showcase"
LABEL org.opencontainers.image.licenses="Apache-2.0"

CMD ["python", "demo/examples/01_basic_query.py"]
