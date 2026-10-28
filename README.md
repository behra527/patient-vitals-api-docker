# Patient Vitals API with Docker

A REST API built with **FastAPI** for recording and retrieving patient vital signs. This project demonstrates API development, input validation, logging, and Docker containerization.

<!-- Badges -->
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-4051B5)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Development-orange)

## Features

- Record patient vital signs through a REST API
- Retrieve vitals by patient ID
- List records with a configurable limit
- Health check endpoint
- Request validation using Pydantic
- Configurable logging through environment variables
- Interactive API documentation with Swagger UI
- Docker image for consistent deployment
- Non-root user configured inside the Docker container

## Tech Stack

- Python 3.12
- FastAPI
- Pydantic
- Uvicorn
- Docker

## Project Structure

```text
patient-vitals-api-docker/
├── app/
│   ├── __init__.py
│   └── main.py
├── .dockerignore
├── .env
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

## Run with Docker

### Pull the Image

```bash
docker pull behram527/patient-vitals-api:1.0
```

### Start the Container

```bash
docker run -d \
  --name patient-vitals-api \
  -p 8000:8000 \
  -e LOG_LEVEL=DEBUG \
  behram527/patient-vitals-api:1.0
```

### Verify the Container

```bash
docker ps
docker logs patient-vitals-api
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API information |
| GET | `/health` | Health check |
| POST | `/vitals` | Record patient vitals |
| GET | `/vitals/{patient_id}` | Retrieve a patient's vitals |
| GET | `/vitals?limit=20` | List recorded vitals |

## Example Request

Send a `POST` request to `/vitals` with this JSON body:

```json
{
  "patient_id": "P001",
  "heart_rate": 78,
  "temperature": 36.8,
  "systolic_bp": 120,
  "diastolic_bp": 80,
  "spo2": 98
}
```

Example using curl:

```bash
curl -X POST "http://localhost:8000/vitals" \
  -H "Content-Type: application/json" \
  -d '{"patient_id":"P001","heart_rate":78,"temperature":36.8,"systolic_bp":120,"diastolic_bp":80,"spo2":98}'
```

## Interactive Documentation

When the container is running, open:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## Configuration

The application supports the `LOG_LEVEL` environment variable.

Example:

```bash
-e LOG_LEVEL=DEBUG
```

Supported Python logging levels include `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`.

## Build the Image Locally

```bash
docker build -t patient-vitals-api:1.0 .
```

## Stop and Remove the Container

```bash
docker stop patient-vitals-api
docker rm patient-vitals-api
```

## Limitations and Security

- This demo stores data in memory; records are lost when the application restarts.
- The API is intended for educational and demonstration purposes.
- Do not submit real patient information.
- Production systems require persistent storage, authentication, authorization, encryption, and appropriate healthcare privacy controls.

## Docker Hub

Docker image: [behram527/patient-vitals-api](https://hub.docker.com/r/behram527/patient-vitals-api)

