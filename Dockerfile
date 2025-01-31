FROM python:3.9-slim as backend

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "backend.api.routes.chat:router", "--host", "0.0.0.0", "--port", "8000"]
