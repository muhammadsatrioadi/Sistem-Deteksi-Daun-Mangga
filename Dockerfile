FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    YOLO_CONFIG_DIR=/app/.ultralytics

WORKDIR /app

# Dependensi sistem untuk OpenCV / Ultralytics
RUN apt-get update && apt-get install -y --no-install-recommends \
        libglib2.0-0 \
        libgl1 \
        libsm6 \
        libxext6 \
        libxrender1 \
        fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# PyTorch versi CPU (server tanpa GPU, ukuran image lebih kecil)
RUN pip install --no-cache-dir torch torchvision \
        --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/.ultralytics /app/static/uploads

EXPOSE 5000

# Server produksi: gunicorn (1 worker, multi-thread) memuat model best.pt sekali
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--worker-class", "gthread", \
     "--workers", "1", "--threads", "4", "--timeout", "180", "app:app"]
