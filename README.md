# Node.js and Python Microservices

A microservices-based application that demonstrates communication between a Node.js Express server and a Python FastAPI service.

## Features

- **PDF to Image Conversion**: Convert PDF files to images using Python
- **PDF Text Extraction**: Extract structured text data from PDF files
- **Microservices Architecture**: Separate Node.js and Python services communicating via HTTP

## Project Structure

```
node-python/
├── docker-compose.yml
├── node-app/
│   ├── app.js                 # Main Node.js application
│   ├── routes/
│   │   └── pdf-routes.js      # PDF operation routes
│   ├── Dockerfile
│   └── package.json
├── python-app/
│   ├── main.py                # Main FastAPI application
│   ├── routes/
│   │   └── pdf_routes.py      # PDF operation routes
│   ├── utils/
│   │   └── text_extractor.py  # PDF text extraction utilities
│   ├── Dockerfile
│   └── requirements.txt
└── file/                      # Shared files directory
```

## API Endpoints

### Node.js API (Express)

- `GET /`: Welcome message
- `POST /api/convert-pdf`: Convert PDF to image
  - Request body: `{ "pdfPath": "path/to/pdf" }`
  - Response: `{ "success": true, "imagePath": "path/to/image", "message": "PDF successfully converted to image" }`
- `POST /api/extract-text`: Extract structured text from PDF
  - Request body: `{ "pdfPath": "path/to/pdf" }`
  - Response: `{ "success": true, "data": { "status": true, "data": { ... patient details ... } }, "message": "PDF text successfully extracted" }`

### Python API (FastAPI)

- `GET /`: Welcome message
- `POST /api/convert-pdf`: Convert PDF to image
  - Request body: `{ "pdf_path": "path/to/pdf" }`
  - Response: `{ "image_path": "path/to/image" }`
- `POST /api/extract-text`: Extract text from PDF
  - Request body: `{ "pdf_path": "path/to/pdf" }`
  - Response: `{ "status": true, "data": { ... patient details ... } }`

## Getting Started

1. Clone the repository
2. Run the services with Docker Compose:
   ```bash
   docker-compose up
   ```
3. Access the Node.js API at http://localhost:3000
4. Access the Python API at http://localhost:5000

## Dependencies

### Node.js
- Express
- Axios

### Python
- FastAPI
- Uvicorn
- PyMuPDF
- pdf2image
- poppler-utils
- Pydantic 