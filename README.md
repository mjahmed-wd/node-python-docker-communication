# Docker Compose Project

This project demonstrates a simple web application using Docker Compose with two services:
1. A Node.js Express server
2. A Python Flask server

## Project Structure

```
node-python/
├── docker-compose.yml
├── file/
│   └── print-preview.pdf
├── node-app/
│   ├── app.js
│   ├── package.json
│   └── Dockerfile
└── python-app/
    ├── app.py
    ├── requirements.txt
    └── Dockerfile
```

## Running the Application

To start both services, run:

```bash
docker-compose up
```

To build and start in detached mode:

```bash
docker-compose up --build -d
```

## Services

### Node.js Express Server
- URL: http://localhost:3000
- Returns: "Hello from Node.js!"

### Python Flask Server
- URL: http://localhost:5000
- Returns: "Hello from Python!"

## Stopping the Application

To stop the services:

```bash
docker-compose down
``` 