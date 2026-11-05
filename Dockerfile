FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

WORKDIR /app

RUN pip install "fastmcp==4.1.6"

COPY server.py .

RUN useradd --create-home --uid 10001 appuser
USER 10001

EXPOSE 8000

CMD ["python", "server.py"]
