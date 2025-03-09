from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pdf2image import convert_from_path
import os
import time
from pydantic import BaseModel
# Using the alternative text extractor that doesn't rely on PyMuPDF
# from utils.text_extractor_alt import extract_text_from_pdf
from utils.text_extractor import get_text_from_pdf, convert_pdf_to_txt

router = APIRouter()

class PdfRequest(BaseModel):
    pdf_path: str

@router.post("/convert-pdf")
def convert_pdf(request: PdfRequest):
    """
    Endpoint to convert PDF to image
    """
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


@router.post("/extract-text")
def extract_text(request: PdfRequest):
    """
    Endpoint to extract text and patient details from PDF
    
    This endpoint extracts both structured patient data and raw text from a PDF file.
    """
    try:
        pdf_path = request.pdf_path
        
        # Handle relative paths correctly inside the container
        if not pdf_path.startswith('/'):
            actual_path = os.path.join('/app', pdf_path)
        else:
            actual_path = pdf_path
        
        print(f"Looking for PDF at: {actual_path}")
        
        # Check if the file exists
        if not os.path.exists(actual_path):
            raise HTTPException(status_code=404, detail=f"PDF file not found: {pdf_path} (resolved to {actual_path})")
        
        # First convert PDF to text
        text_content = convert_pdf_to_txt(actual_path)
        
        # Then extract structured data from the text content
        result = get_text_from_pdf(text_content)
        
        # Parse the result to get the JSON data
        # The result is in format "[(status)]{json_data}"
        import json
        import re
        
        # Extract status and JSON data
        match = re.match(r'\[\((\d)\)\](.*)', result)
        if match:
            status = match.group(1)
            json_str = match.group(2)
            
            # Parse the JSON string into a Python dict
            parsed_data = json.loads(json_str)
            
            # Check which critical fields are missing
            missing_fields = []
            critical_fields = ["Patient", "Patient ID", "Date of Birth", "Test Type"]
            for field in critical_fields:
                if not parsed_data.get(field):
                    missing_fields.append(field)
            
            # Format the response as requested
            if status == "1":
                message = "PDF text extraction successful"
            else:
                if missing_fields:
                    message = f"PDF text extraction partially successful. Missing critical fields: {', '.join(missing_fields)}"
                else:
                    message = "PDF text extraction partially successful, some data may be missing"
            
            return {
                "data": {
                    "text": parsed_data
                },
                "message": message
            }
        else:
            return {
                "data": {
                    "text": {}
                },
                "message": "Error parsing PDF extraction result"
            }
    
    except Exception as e:
        return {
            "data": {
                "text": {}
            },
            "message": f"Error extracting text from PDF: {str(e)}"
        } 