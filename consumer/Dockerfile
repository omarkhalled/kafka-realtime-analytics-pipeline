FROM python:3.10-slim

WORKDIR /app

COPY consumer.py .

ENV PYTHONUNBUFFERED=1
RUN pip install kafka-python elasticsearch==8.12.0

CMD ["python", "consumer.py"]
