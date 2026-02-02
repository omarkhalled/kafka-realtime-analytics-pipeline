FROM python:3.10-slim

WORKDIR /app
COPY producer.py .
ENV PYTHONUNBUFFERED=1
RUN pip install kafka-python

CMD ["python", "producer.py"]
