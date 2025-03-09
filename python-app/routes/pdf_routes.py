from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pdf2image import convert_from_path
import os
import time
from pydantic import BaseModel
from utils.text_extractor import get_text_from_pdf, convert_pdf_to_txt
from utils.image_extractor import extract_images_from_pdf
from fastapi.staticfiles import StaticFiles

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

@router.post("/extract-images")
def extract_images(request: PdfRequest):
    """
    Endpoint to extract visualization images from PDF files
    
    This endpoint extracts various visualization images from a PDF file,
    saves them to the local filesystem, and returns URLs to access them.
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
        
        # Create a unique directory for this extraction within the static folder
        timestamp = int(time.time())
        extraction_dir = f"extracted_images_{timestamp}"
        output_dir = os.path.join('/app/static', extraction_dir)
        
        # Extract images from the PDF
        result = extract_images_from_pdf(actual_path, output_dir)
        
        # Generate URLs for each image
        base_url = f"/static/{extraction_dir}"
        images_with_urls = []
        
        for image in result["images"]:
            if image["success"]:
                image_url = f"{base_url}/{image['filename']}"
                images_with_urls.append({
                    "type": image["type"],
                    "url": image_url,
                    "filename": image["filename"],
                    "description": get_image_description(image["type"])
                })
        
        return {
            "data": {
                "images": images_with_urls,
                "pdf_path": actual_path,
                "extraction_time": timestamp
            },
            "message": "Images successfully extracted" if result["status"] else "Some images could not be extracted"
        }
    
    except Exception as e:
        return {
            "data": {
                "images": []
            },
            "message": f"Error extracting images from PDF: {str(e)}"
        }

def get_image_description(image_type):
    """
    Return a human-readable description of the image type
    """
    descriptions = {
        "gray_scale": "Grayscale visualization of the visual field test",
        "sensitivity_values": "Numerical sensitivity values across the visual field",
        "total_deviation_values": "Total deviation values showing differences from normal values",
        "pattern_deviation_values": "Pattern deviation values showing localized defects",
        "td_probability_values": "Total deviation probability values indicating statistical significance",
        "pd_probability_values": "Pattern deviation probability values indicating statistical significance",
        "legend": "Legend explaining symbols and color codes used in the visualizations"
    }
    
    return descriptions.get(image_type, "Visual field test image") 