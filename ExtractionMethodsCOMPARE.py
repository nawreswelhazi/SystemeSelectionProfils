# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 21:23:53 2023

@author: NAWRESS
"""

import pandas as pd
import numpy as np
from glob import glob
from tqdm.notebook import tqdm
import matplotlib.pyplot as plt
from PIL import Image
import datetime

plt.style.use('ggplot')


IMGs = glob('C:/Users/NAWRESS/python/CVIMG/*')
for i in range(1) :
    fig, axs = plt.subplots(figsize=(100,50))
    axs.imshow(plt.imread(IMGs[i]))
    img_id = IMGs[i].split('/')[-1].split('-')[:-1]
    img_id1 = "".join(img_id)
    axs.set_title(f'{img_id1}')
    print(img_id1)
    plt.show()
    
#Pytesseract
import pytesseract
now = datetime.datetime.now()
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
pytesseract.image_to_string(IMGs[0], lang='eng')
print("Extraction Tesseract")
print("L'extraction a commencé à ", now)
print("Extraction Tesseract Done à", datetime.datetime.now())


#EasyOCR
print("Extraction EasyOCR")
import easyocr
now = datetime.datetime.now()
reader = easyocr.Reader(['en'], gpu = False)
results = reader.readtext(IMGs[0])
easyocrDF = pd.DataFrame(results, columns=['bbox', 'text','confidence'])
print("L'extraction a commencé à ", now)
print("Extraction EasyOCR Done à", datetime.datetime.now())

#easy_results=easyocrDF.query(expr, kwargs)
