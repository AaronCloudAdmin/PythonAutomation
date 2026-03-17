import pytesseract

from PIL import Image

import csv

import re

 

# Point to your Tesseract install (Windows)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

 

HEADER_TOKENS_FIRST = re.compile(r'^(first(\s*name)?|preferred\s*/?\s*first|given(\s*name)?)$', re.I)

HEADER_TOKENS_LAST  = re.compile(r'^(last(\s*name)?|name\s*last\s*name|surname|family(\s*name)?)$', re.I)

 

def image_to_csv(image_path, output_csv):

    img = Image.open(image_path)

    raw_text = pytesseract.image_to_string(img)

 

    print("Raw OCR output:\n", raw_text)

 

    names = []

    for line in raw_text.strip().splitlines():

        line = line.strip()

        if not line:

            continue

 

        # --- existing simple parsing (FirstName LastName) ---

        parts = line.split()

        if len(parts) >= 2:

            first = parts[0].strip(' "\'')

            last  = " ".join(parts[1:]).strip(' "\'')

 

            # Skip header-like rows such as:

            #   "Preferred/First" , "Name Last Name"

            #   "First Name"      , "Last Name"

            if HEADER_TOKENS_FIRST.fullmatch(first) or HEADER_TOKENS_LAST.fullmatch(last):

                continue

 

            # Also skip “pure header” lines that say both

            both = (first + " " + last).lower()

            if re.search(r'\b(first\s*name|firstname|preferred/?\s*first|given\s*name)\b', both) and \

               re.search(r'\b(last\s*name|lastname|surname)\b', both):

                continue

 

            names.append((first, last))

 

    # Write exactly one header row

    with open(output_csv, 'w', newline='', encoding='utf-8') as f:

        writer = csv.writer(f)

        writer.writerow(['FirstName', 'LastName'])

        writer.writerows(names)

 

    print(f"Saved {len(names)} names to {output_csv}")

 

# Usage

image_to_csv(

    r'C:\Path\To\names.jpg',

    r'C:\Path\To\names.csv'

)

 

import subprocess

 

subprocess.run([

    "powershell.exe",

    "-NoProfile",

    "-ExecutionPolicy", "Bypass",

    "-File", r"C:Path\To\PowerShell_Script.ps1"

])