# odw2json: PDF -> JSON for KIO appeal cases. CPU only, no GPU, no external services.
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONUTF8=1 PIP_NO_CACHE_DIR=1
# runtime libraries of opencv-python-headless and onnxruntime (RapidOCR)
RUN apt-get update \
 && apt-get install -y --no-install-recommends libglib2.0-0 libgomp1 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
# fetch the RapidOCR ONNX models at build time, so OCR works offline at run time
RUN python -c "from rapidocr import RapidOCR; RapidOCR()"

COPY odw2json/ odw2json/
COPY recipes/ recipes/
COPY profiles/ profiles/
COPY dictionaries/ dictionaries/
COPY schemas/ schemas/
COPY web/ web/

RUN mkdir -p /app/input /app/output
EXPOSE 8000
# default: the web UI; the compose service "cli" overrides the command
CMD ["python", "-m", "web", "--host", "0.0.0.0", "--port", "8000"]
