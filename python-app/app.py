from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pdf2image import convert_from_path
import os
import time
from pydantic import BaseModel

app = FastAPI()

class PdfRequest(BaseModel):
    pdf_path: str

@app.get("/")
def read_root():
    return {"message": "Hello from Python FastAPI!"}

@app.post("/api/convert-pdf")
def convert_pdf(request: PdfRequest):
    try:
        pdf_path = request.pdf_path
        
        # Handle relative paths correctly inside the container
        # If the path doesn't start with /, assume it's relative to /app
        if not pdf_path.startswith('/'):
            actual_path = os.path.join('/app', pdf_path)
        else:
            actual_path = pdf_path
        
        print(f"Looking for PDF at: {actual_path}")
        
        # Check if the file exists
        if not os.path.exists(actual_path):
            raise HTTPException(status_code=404, detail=f"PDF file not found: {pdf_path} (resolved to {actual_path})")
        
        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.path.dirname(actual_path), "converted_images")
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate a unique filename using timestamp
        timestamp = int(time.time())
        output_image_path = os.path.join(output_dir, f"converted_{timestamp}.jpg")
        
        # Convert PDF to image (first page only)
        images = convert_from_path(actual_path, first_page=1, last_page=1)
        
        # Save the image
        if images:
            images[0].save(output_image_path, 'JPEG')
            return {"image_path": output_image_path}
        else:
            raise HTTPException(status_code=500, detail="Failed to convert PDF to image")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000) 