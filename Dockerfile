FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Esta es la orden que le dice a Render que use tu script directamente
CMD ["python", "bot.py"]
