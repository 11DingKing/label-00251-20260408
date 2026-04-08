FROM --platform=$BUILDPLATFORM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn eventlet

FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

RUN mkdir -p instance

EXPOSE 5001

CMD ["sh", "-c", "python reset_db.py 2>/dev/null || true; gunicorn -k eventlet -w 1 -b 0.0.0.0:5001 run:app"]
