# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 20:10:53 2023

@author: NAWRESS
"""

import cv2
import matplotlib.pyplot as plt
import pytesseract
import numpy as np
from glob import glob
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

#dilate img
def dilate(img):
    #Specify structure shape and kernel size
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,50))
    #Applying dilation on the threshold image
    dilation = cv2.dilate(img, rect_kernel, iterations = 1)
    return (dilation)

def contours(img):
    #Finding contours
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours
    
def extractText(img, contours):
    #Creating a copy of image
    im2 = img.copy()
    #Affichage des contours sur la photo copie im2 using openCV
    text = ""
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        rect = cv2.rectangle(im2, (x,y), (x+w, y+h), (0,255,0), 2)
        cropped = im2[y:y+h, x:x+w]
        #configure tesseract params
        #psm : page segmentation mode, 6 : Assume a single uniform bloc of text
        #oem : Engine mode, 3: Default, based on what is available
        custom_config = r'--oem 1 --psm 3'
        text = pytesseract.image_to_string(cropped, config=custom_config) + text + "\n"
    return im2
    
    

img_dir = glob('C:/Users/NAWRESS/python/CVIMG/*.jpg')
for i in img_dir:
    img_id = i.split('\\')[-1]
    img = cv2.imread(r'C:/Users/NAWRESS/python/CVIMG/'+img_id)
    grayIMG = gray(img)
    thresh1 = threshold(grayIMG)
    dilated = dilate(thresh1)
    contours1 = contours(dilated)
    im2 = extractText(img, contours1) 
    cv2.namedWindow('image3', cv2.WINDOW_NORMAL)
    cv2.imshow('image3',im2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

        