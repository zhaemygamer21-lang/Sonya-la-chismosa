FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 10000
# Esta línea obliga a Flask a abrir el puerto 10000 de inmediato
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=10000"]
