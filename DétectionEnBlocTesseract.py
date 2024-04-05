# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 17:11:38 2023

@author: NAWRESS
"""

import cv2
import matplotlib.pyplot as plt
import pytesseract
from pytesseract import Output
import numpy as np
from glob import glob
from pathlib import Path
import os
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
cv2.__version__

#Convert the image to gray scale
def gray(img):
    grayIMG = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return grayIMG
    
#Performing OTSU threshold
def threshold(img): 
    ret, thresh1 = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    return thresh1

def extractData(img):
    custom_config = r' --psm 3'
    details = pytesseract.image_to_data(img, output_type=Output.DATAFRAME)
    return details

def drawContour(details):
    im2 = img.copy()
    for i in range(len(details['level'])) :
        (x,y,w,h) = (details['left'][i], details['top'][i], details['width'][i], details['height'][i])
        cv2.rectangle(im2, (x,y), (x+w, y+h), (0, 255, 0), 2)
    return im2
    
Imagesave_dir = Path('C:/Users/NAWRESS/python/ContouredImages')  
DatapathSave = 'C:/Users/NAWRESS/python/ImageData'
img_dir = glob('C:/Users/NAWRESS/python/CVIMG/*.jpg')
for i in img_dir:
    img_id = i.split('\\')[-1]
    img = cv2.imread(r'C:/Users/NAWRESS/python/CVIMG/'+img_id)
    grayIMG = gray(img)
    thresh1 = threshold(grayIMG)
    details = extractData(thresh1)
    # saving as tsv file
    img_id1 = img_id.split('.jpg')[0]
    details.to_csv(os.path.join(DatapathSave, f'example_{img_id1}.tsv'), sep="\t")
    im2 = drawContour(details)
    os.chdir(Imagesave_dir)
    cv2.imwrite(f'{img_id}.jpg',im2)

