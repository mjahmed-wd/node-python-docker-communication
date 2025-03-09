#!/usr/bin/env python3
import fitz
import re
import json
import sys


def convert_pdf_to_txt(file_path):
    doc = fitz.open(file_path)  # open document
    output_txt = b""  # initialize as bytes
    
    for page in doc:  # iterate the document pages
        # get plain text and encode to UTF-8 bytes
        page_text = page.get_text().encode("utf8")
        output_txt += page_text
        # Add a page delimiter
        output_txt += bytes((12,))  # form feed character as page delimiter
    
    return output_txt


def get_text_from_pdf(lines):
    patient_details = {
        "Patient": None,
        "Date of Birth": None,
        "Gender": None,
        "Patient ID": None,
        "Office Location": None,
        "Test Type": None,
        "Created": None,
        "Fixation Monitor": None,
        "Fixation Target": None,
        "Fixation Losses": None,
        "False POS Errors": None,
        "False NEG Errors": None,
        "Test Duration": None,
        "Fovea": None,
        "Stimulus": None,
        "Background": None,
        "Strategy": None,
        "Pupil Diameter": None,
        "Visual Acuity": None,
        "Rx": None,
        "Date": None,
        "Time": None,
        "Age": None,
        # Additional fields that might be present in PDFs
        "Eye": None,
        "Grid": None,
        "MD10-2": None,
        "PSD10-2": None,
        "SF": None,
        "CPSD": None,
        # Other possible visual field metrics
        "MD": None,
        "PSD": None,
        "VFI": None,
        "GHT": None,
    }
    emptyString = ""

    lines = lines.decode("utf-8")
    lines = lines.splitlines()
    # print(lines)
    i = 0
    while i < len(lines):
        if ":" in lines[i]:
            newData = lines[i].split(":", 1)
            if newData[1].strip() != emptyString:
                if newData[0] in patient_details.keys():
                    if not re.search("/\d+/", newData[0]):
                        answer = newData[1].replace(",", "")
                        answer = answer.strip()
                        patient_details[newData[0]] = answer
                i = i + 1
            else:
                tempArray = []
                if lines[i + 1].strip()[len(lines[i + 1].strip()) - 1] == ":":
                    while True:
                        nextData = lines[i].split(":")
                        tempArray.append(nextData[0])
                        i = i + 1
                        if lines[i][len(lines[i].strip()) - 1] != ":":
                            break

                    for data in tempArray:
                        if data in patient_details.keys():
                            if not re.search("/\d+/", data):
                                if data == "Pupil Diameter":
                                    if "mm" in lines[i]:
                                        answer = lines[i].replace(",", "")
                                        answer = answer.strip()
                                        patient_details[data] = answer
                                        i = i + 1
                                else:
                                    answer = lines[i].replace(",", "")
                                    answer = answer.strip()
                                    patient_details[data] = answer
                                    i = i + 1
                    tempArray.clear()
                else:
                    if "dB" in lines[i+1]:
                        answer = str(re.match("(.*?)dB", lines[i + 1]).group())
                    else:
                        answer = lines[i+1]
                    answer = answer.replace(",", "")
                    answer = answer.strip()
                    patient_details[newData[0]] = answer
                    i = i + 1
        else:
            pattern = "[0-9]+[ |[a-zà-ú.,-]* ((highway)|(autoroute)|(north)|" \
                    "(nord)|(south)|(sud)|(east)|(est)|(west)|(ouest)|(avenue)|" \
                    "(lane)|(voie)|(ruelle)|(road)|(rue)|(route)|(drive)|" \
                    "(boulevard)|(circle)|(cercle)|(street)|(cer\.)|(cir\.)|" \
                    "(blvd\.)|(hway\.)|(st\.)|(aut\.)|(ave\.)|(ln\.)|(rd\.)|" \
                    "(hw\.)|(dr\.)|(a\.))([ .,-]*[a-zà-ú0-9]*)*"
            match = re.match(pattern, lines[i], re.IGNORECASE)
            if match:
                patient_details["Office Location"] = match.group()
                tempString = lines[i+1]+" "+lines[i+2]+" "+lines[i+3]
                if(re.match("(^|OS|OD).+(Test|$)",tempString)):
                    tempEyeAndGridArray = tempString.split("Single Field Analysis")
                    patient_details["Eye"] = tempEyeAndGridArray[0].strip()
                    patient_details["Test Type"] = tempEyeAndGridArray[1].strip()
                    patient_details["Grid"] = tempEyeAndGridArray[1].strip().split(" ")[1].strip()
            
            # Check for visual field metrics (MD, PSD, etc.)
            for metric in ["MD", "PSD", "VFI", "SF", "CPSD", "MD10-2", "PSD10-2"]:
                if metric in lines[i]:
                    # Try to extract the value with dB unit
                    match = re.search(r'{}[:\s]*([-+]?\d+\.\d+)\s*dB'.format(metric), lines[i], re.IGNORECASE)
                    if match:
                        patient_details[metric] = match.group(1) + " dB"
            
            i = i + 1

    if patient_details["Patient ID"]:
        # response = {'status': True, 'data': json.dumps(patient_details)}
        response = "[(1)]" + json.dumps(patient_details)
        return response
    else:
        # response = {'status': False, 'data': json.dumps(patient_details)}
        response = "[(0)]" + json.dumps(patient_details)
        return response


if __name__ == "__main__":
    # file_path = "patients/patient_1"
    pdf_file = sys.argv[1]
    txt_data = convert_pdf_to_txt(pdf_file)
    patient_details = get_text_from_pdf(txt_data)

    print(patient_details)
