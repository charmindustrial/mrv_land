# qa-trigger image. deploy.sh stages trigger/* plus ../qa_inputs.py.
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py qa_inputs.py ./
CMD exec gunicorn --bind ":${PORT:-8080}" --workers 1 --threads 4 main:app
