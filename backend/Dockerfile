FROM python:3.11-slim

WORKDIR /app

COPY script.py /app

# Install dependencies
RUN pip install flask flask-cors requests

EXPOSE 5000

CMD ["python", "script.py"]
