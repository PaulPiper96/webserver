FROM python:3.12-slim

WORKDIR /app

# Dependencies zuerst (bessere Docker-Cache-Nutzung)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App-Code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]