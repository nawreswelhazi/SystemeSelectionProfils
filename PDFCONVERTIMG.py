# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 16:04:41 2023

@author: NAWRESS
"""


# import module
from pdf2image import convert_from_path
from pathlib import Path
 
pdf_dir = Path('C:/Users/NAWRESS/python//CVS')
save_dir = Path('C:/Users/NAWRESS/python/CVIMG')

for pdf_file in pdf_dir.glob('*.pdf'):
    pages = convert_from_path(pdf_file, 300, poppler_path=r'C:/Program Files/poppler-23.01.0/Library/bin')
    for num, page in enumerate(pages, start=1):
        page.save(save_dir / f'{pdf_file.stem}-page{num}.jpg', 'JPEG')

