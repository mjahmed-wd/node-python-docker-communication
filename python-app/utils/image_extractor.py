#!/usr/bin/env python3
import fitz
import os
from PIL import Image, ImageDraw
import json
import sys
import time


def convert_pdf2img(input_file: str):
    # Open the document
    pdfIn = fitz.open(input_file)

    # Select a page
    page = pdfIn[0]
    rotate = int(0)
    zoom_x = 2
    zoom_y = 2

    mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    image_data = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    pdfIn.close()

    return image_data


def get_gray_scale(img, output_path: str):
    # crop image
    width, height = img.size
    x = (width - height)//2
    img_cropped = img.crop((653, 430, x+height, height))

    # create grayscale image
    mask = Image.new('L', img_cropped.size)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, 382, 390), fill=255)

    # add mask as alpha channel
    img_cropped.putalpha(mask)
    
    # Trim unnecessary whitespace
    img_cropped = trim_whitespace(img_cropped)
    
    flag = None
    try:
        imagePath = os.path.join(output_path, 'gray_scale_image.png')
        img_cropped.save(imagePath)
        flag = True
    except ValueError as e:
        print(f"Error saving gray scale image: {e}")
        flag = False

    return flag, 'gray_scale_image.png'


def get_sensitivity_values(img, output_path: str):
    # crop image
    width, height = img.size
    x = (width - height)//2
    img_cropped = img.crop((245, 425, x+height, height))

    # create grayscale image
    mask = Image.new('L', img_cropped.size)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, 382, 390), fill=255)

    # add mask as alpha channel
    img_cropped.putalpha(mask)
    
    # Trim unnecessary whitespace
    img_cropped = trim_whitespace(img_cropped)
    
    flag = None
    try:
        imagePath = os.path.join(output_path, "sensitivity_values_image.png")
        img_cropped.save(imagePath)
        flag = True
    except Exception as e:
        print(f"Error saving sensitivity values image: {e}")
        flag = False

    return flag, 'sensitivity_values_image.png'


def get_total_deviation_values(img, output_path: str):
    # crop image
    width, height = img.size
    x = (width - height)//2
    img_cropped = img.crop((121, 761, x+height, height))

    # create grayscale image
    mask = Image.new('L', img_cropped.size)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, 260, 270), fill=255)

    # add mask as alpha channel
    img_cropped.putalpha(mask)
    
    # Trim unnecessary whitespace
    img_cropped = trim_whitespace(img_cropped)
    
    flag = None
    try:
        imagePath = os.path.join(output_path, "total_deviation_values_image.png")
        img_cropped.save(imagePath)
        flag = True
    except Exception as e:
        print(f"Error saving total deviation values image: {e}")
        flag = False
    return flag, 'total_deviation_values_image.png'


def get_pattern_deviation_values(img, output_path: str):
    # crop image
    width, height = img.size
    x = (width - height)//2
    img_cropped = img.crop((487, 762, x+height, height))

    # create grayscale image
    mask = Image.new('L', img_cropped.size)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, 260, 270), fill=255)

    # add mask as alpha channel
    img_cropped.putalpha(mask)
    
    # Trim unnecessary whitespace
    img_cropped = trim_whitespace(img_cropped)
    
    flag = None
    try:
        imagePath = os.path.join(output_path, "pattern_deviation_values_image.png")
        img_cropped.save(imagePath)
        flag = True
    except Exception as e:
        print(f"Error saving pattern deviation values image: {e}")
        flag = False
    return flag, 'pattern_deviation_values_image.png'


def get_td_probability_values(img, output_path: str):
    # crop image
    width, height = img.size
    x = (width - height)//2
    img_cropped = img.crop((125, 1046, x+height, height))

    # create grayscale image
    mask = Image.new('L', img_cropped.size)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, 260, 270), fill=255)

    # add mask as alpha channel
    img_cropped.putalpha(mask)
    
    # Trim unnecessary whitespace
    img_cropped = trim_whitespace(img_cropped)
    
    flag = None
    try:
        imagePath = os.path.join(output_path, "TD_probability_values_image.png")
        img_cropped.save(imagePath)
        flag = True
    except Exception as e:
        print(f"Error saving TD probability values image: {e}")
        flag = False
    return flag, 'TD_probability_values_image.png'


def get_pd_probability_values(img, output_path: str):
    # crop image
    width, height = img.size
    x = (width - height)//2
    img_cropped = img.crop((493, 1046, x+height, height))

    # create grayscale image
    mask = Image.new('L', img_cropped.size)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, 260, 270), fill=255)

    # add mask as alpha channel
    img_cropped.putalpha(mask)
    
    # Trim unnecessary whitespace
    img_cropped = trim_whitespace(img_cropped)
    
    flag = None
    try:
        imagePath = os.path.join(output_path, "PD_probability_values_image.png")
        img_cropped.save(imagePath)
        flag = True
    except Exception as e:
        print(f"Error saving PD probability values image: {e}")
        flag = False
    return flag, 'PD_probability_values_image.png'


def get_legend(img, output_path: str):
    # crop image
    width, height = img.size
    x = (width - height)//2
    # Adjusting crop coordinates to better focus on the legend content
    img_cropped = img.crop((1010, 1185, 1010 + 130, 1185 + 130))

    # create grayscale image
    mask = Image.new('L', img_cropped.size)
    mask_draw = ImageDraw.Draw(mask)
    
    # Using rectangle
    mask_draw.rectangle((0, 0, 130, 130), fill=255)
    
    # add mask as alpha channel
    img_cropped.putalpha(mask)
    
    # Trim unnecessary whitespace with smaller padding to reduce empty space
    img_cropped = trim_whitespace(img_cropped)
    
    flag = None
    try:
        imagePath = os.path.join(output_path, "legend_image.png")
        img_cropped.save(imagePath)
        flag = True
    except Exception as e:
        print(f"Error saving legend image: {e}")
        flag = False
    return flag, 'legend_image.png'


def trim_whitespace(image):
    """
    Trims the whitespace around an image to only keep the content.
    
    Args:
        image: PIL Image object
    
    Returns:
        Trimmed PIL Image object
    """
    # Make sure the image is in RGBA mode for alpha channel
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # Create a new white background image
    bg = Image.new('RGBA', image.size, (255, 255, 255, 0))
    
    # Paste the image on the background using the alpha as mask
    bg.paste(image, (0, 0), image)
    
    # Get the data as a numpy array
    data = bg.getdata()
    
    # Find the bounds of non-transparent pixels
    non_empty_columns = []
    non_empty_rows = []
    
    for y in range(image.height):
        for x in range(image.width):
            if data[y * image.width + x][3] > 0:  # If alpha channel is not 0
                non_empty_rows.append(y)
                non_empty_columns.append(x)
    
    if not non_empty_rows or not non_empty_columns:
        return image  # Return original if no non-transparent pixels found
    
    # Get the bounds - using smaller padding (2px instead of 5px)
    min_x = max(0, min(non_empty_columns) - 2)
    max_x = min(image.width, max(non_empty_columns) + 2)
    min_y = max(0, min(non_empty_rows) - 2)
    max_y = min(image.height, max(non_empty_rows) + 2)
    
    # Crop the image
    return image.crop((min_x, min_y, max_x, max_y))


def extract_images_from_pdf(pdf_file, output_path):
    """
    Extract images from a PDF file and save them to the specified output path.
    Returns information about the extracted images.
    """
    # Make sure output directory exists
    os.makedirs(output_path, exist_ok=True)
    
    # Converting pdf to img
    pixData = convert_pdf2img(pdf_file)
    
    # Dictionary to store image information
    image_info = {
        "images": []
    }
    
    # Extract all image types
    extraction_functions = [
        ("gray_scale", get_gray_scale),
        ("sensitivity_values", get_sensitivity_values),
        ("total_deviation_values", get_total_deviation_values),
        ("pattern_deviation_values", get_pattern_deviation_values),
        ("td_probability_values", get_td_probability_values),
        ("pd_probability_values", get_pd_probability_values),
        ("legend", get_legend)
    ]
    
    all_successful = True
    
    for image_type, extraction_func in extraction_functions:
        success, filename = extraction_func(pixData, output_path)
        if not success:
            all_successful = False
        
        image_info["images"].append({
            "type": image_type,
            "filename": filename,
            "path": os.path.join(output_path, filename),
            "success": success
        })
    
    image_info["status"] = all_successful
    
    return image_info


if __name__ == "__main__":
    # pdf file path
    pdf_file = sys.argv[1]
    
    # Output directory - make it optional with default value
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    else:
        output_path = "output"  # Default output directory
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Get response
    res = extract_images_from_pdf(pdf_file, output_path)
    print(res)

    # for data in res.keys():
    #     if res["status"]:
    #         for img in res["data"]:
    #             print(res["data"][img])

