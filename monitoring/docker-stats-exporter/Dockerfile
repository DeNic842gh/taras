FROM python:3.12-slim-bookworm

WORKDIR /app
COPY requirements.txt exporter.py ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9417
CMD ["python", "exporter.py"]
