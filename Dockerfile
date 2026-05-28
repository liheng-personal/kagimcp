FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir kagimcp==1.0.0 httpx starlette uvicorn

COPY proxy.py .
COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]
