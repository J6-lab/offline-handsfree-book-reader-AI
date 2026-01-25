import cv2
import pytesseract
from PIL import Image
import pdfplumber
import os
import subprocess
from docx import Document

def img_to_text(image_path="page.jpg", output_txt="output.txt"):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    text = pytesseract.image_to_string(Image.fromarray(thresh), config=r'--oem 3 --psm 6')

    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(text)

def pdf_to_text_pagewise(pdf_path, output_txt):
    with pdfplumber.open(pdf_path) as pdf:
        with open(output_txt, "w", encoding="utf-8") as f:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    f.write(t + "\n")

def word_to_txt(file_path, output_txt="output.txt"):
    ext = os.path.splitext(file_path.lower())[1]

    if ext == ".docx":
        doc = Document(file_path)
        with open(output_txt, "w", encoding="utf-8") as f:
            for para in doc.paragraphs:
                f.write(para.text + "\n")

    elif ext == ".doc":
        soffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"
        subprocess.run([soffice_path,"--headless","--convert-to","txt:Text",file_path,"--outdir","."], check=True)
