FROM python:3.12-slim

# Install Chromium + ChromeDriver
RUN apt-get update && apt-get install -y chromium chromium-driver curl unzip && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Run Flask with Gunicorn
CMD ["gunicorn", "server:app", "--bind", "0.0.0.0:10000"]
