#!/usr/bin/env python3
import fitz
import os, io
from PIL import Image, ImageDraw, ImageChops
import base64
from io import BytesIO
import json
import sys
import os


def convert_to_base64(image):
    # Buffer for byte data
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue())


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
    # output_file = f"{os.path.splitext(os.path.basename(input_file))[0]}.png"
    # pix.save(output_file)
    image_data = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    # image_data.show(image_data)
    # print(image_data)
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
        imagePath = output_path+'gray_scale_image.png'
        img_cropped.save(imagePath)
        flag = True
    except ValueError:
        print("STOP:",ValueError)
        flag = False

    return flag
    # gray_scale_image = str(convert_to_base64(img_cropped))
    # return gray_scale_image


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
        img_cropped.save(output_path+"sensitivity_values_image.png")
        flag = True
    except:
        flag = False

    return flag
    # sensitivity_values_image = str(convert_to_base64(img_cropped))
    # return sensitivity_values_image


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
        img_cropped.save(output_path+"total_deviation_values_image.png")
        flag = True
    except:
        flag = False
    return flag
    # total_deviation_values_image = str(convert_to_base64(img_cropped))
    # return total_deviation_values_image


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
        img_cropped.save(output_path+"pattern_deviation_values_image.png")
        flag = True
    except:
        flag = False
    return flag
    # pattern_deviation_values_image = str(convert_to_base64(img_cropped))
    # return pattern_deviation_values_image


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
        img_cropped.save(output_path+"TD_probability_values_image.png")
        flag = True
    except:
        flag = False
    return flag
    # TD_probability_values_image = str(convert_to_base64(img_cropped))
    # return TD_probability_values_image


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
        img_cropped.save(output_path+"PD_probability_values_image.png")
        flag = True
    except:
        flag = False
    return flag
    # PD_probability_values_image = str(convert_to_base64(img_cropped))
    # return PD_probability_values_image


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
        img_cropped.save(output_path+"legend_image.png")
        flag = True
    except:
        flag = False
    return flag
    # legend_image = str(convert_to_base64(img_cropped))
    # return legend_image


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


def generate_response(document, output_path):

    # Converting pdf to img
    pixData = convert_pdf2img(pdf_file)

    # Ensure output_path ends with a slash
    if not output_path.endswith('/'):
        output_path = output_path + '/'

    # image Data storing in a json
    # imageData = {}

    # fetching base64 formatted data in a dictionary
    # imageData["gray_scale_image"] = get_gray_scale(pixData)
    # imageData["sensitivity_values_image"] = get_sensitivity_values(pixData)
    # imageData["total_deviation_values_image"] = get_total_deviation_values(pixData)
    # imageData["pattern_deviation_values_image"] = get_pattern_deviation_values(pixData)
    # imageData["TD_probability_values_image"] = get_td_probability_values(pixData)
    # imageData["PD_probability_values_image"] = get_pd_probability_values(pixData)
    # imageData["legend_image"] = get_legend(pixData)

    gray_scale_image_response = get_gray_scale(pixData, output_path)
    sensitivity_values_image_response = get_sensitivity_values(pixData, output_path)
    total_deviation_values_image_response = get_total_deviation_values(pixData, output_path)
    pattern_deviation_values_image_response = get_pattern_deviation_values(pixData, output_path)
    TD_probability_values_image_response = get_td_probability_values(pixData, output_path)
    PD_probability_values_image_response = get_pd_probability_values(pixData, output_path)
    legend_image_response = get_legend(pixData, output_path)
    # Creating a response
    if gray_scale_image_response and sensitivity_values_image_response and total_deviation_values_image_response and \
                pattern_deviation_values_image_response and TD_probability_values_image_response and PD_probability_values_image_response \
                and legend_image_response: 
        # status = True
        # data = {"gray_scale_image": get_gray_scale(pixData)}
        # arrData = []
        # for image in imageData:
        #     tempDict = {}
        #     tempDict[image] = imageData[image]
        #     arrData.append(tempDict)

        response = {'status': True, 'data': None}
        response = "[(1)]" + json.dumps(response)
        return response
    else:
        response = {'status': False, 'data': None}
        response = "[(0)]" + json.dumps(response)
        return response


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
    res = generate_response(pdf_file, output_path)
    print(res)

    # for data in res.keys():
    #     if res["status"]:
    #         for img in res["data"]:
    #             print(res["data"][img])

