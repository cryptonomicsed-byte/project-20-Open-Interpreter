FROM python:3.11-slim

WORKDIR /app

# Copy FastAPI app (will be created by agent)
COPY app.py .

# Install FastAPI and uvicorn
RUN pip install fastapi uvicorn --no-cache-dir

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
