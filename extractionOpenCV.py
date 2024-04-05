# -*- coding: utf-8 -*-
"""
Created on Tue May  9 15:38:24 2023

@author: NAWRESS
"""

import cv2
import matplotlib.pyplot as plt
import pytesseract
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
   
def ExtractText(img, contours):
    im2 = img.copy()
    list=[]
    textLeft=""
    textRight=""
    maxX=0
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        list.append(x)
        if x>maxX:
            maxX=x
            limit=x+w    
    list.sort()
    array1 = np.asarray(list, dtype = 'int')
    list1 = array1[(array1<limit*0.2)]
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        #rect = cv2.rectangle(im2, (x,y), (x+w, y+h), (0,255,0), 2)
        cropped = im2[y:y+h, x:x+w]
        custom_config = r'--oem 1 --psm 3'
        if x in list1: 
            textLeft = pytesseract.image_to_string(cropped, config=custom_config, lang='fra+eng') + textLeft + "\n"
        else:
            textRight = pytesseract.image_to_string(cropped, config=custom_config, lang='fra+eng') + textRight + "\n"
        #configure tesseract params
        #psm : page segmentation mode, 6 : Assume a single uniform bloc of text
        #oem : Engine mode, 3: Default, based on what is available
    return textLeft, textRight
    
    
def VerticalExtraction(img_dir, Destinationsave_dir):
    img_idPrec = ""
    textRightFinal=""
    for i in img_dir:
        img_id = i.split('\\')[-1] #Enlever le chemin, ne garder que le nom du fichier
        img_idPages = img_id.split('-page')[0] #Ne garder que le nom du cv sans le numero de page
        img = cv2.imread(r'C:/Users/NAWRESS/python/CVIMG/'+img_id)
        if ('_V-' in img_id): #Dans le cas d'un cv en mode Horizental
            os.chdir(Destinationsave_dir) #Où on va stocker les fichiers.txt (résultat final)
            grayIMG = gray(img)
            thresh1 = threshold(grayIMG)
            dilated = dilate(thresh1)
            contours1 = contours(dilated)
            if img_idPages != img_idPrec :
                if (textRightFinal !=""): 
                    file_obj = open(f'{img_idPrec}.txt', "a")
                    file_obj.write(textRightFinal)
                    file_obj.close()
                    textRightFinal=""
                file_obj = open(f'{img_idPages}.txt', "w") #w permet de créer le fichier s'il n'existe pas
                textLeft, textRight= ExtractText(img,contours1)
                textRightFinal+=textRight+"\n"
                file_obj.write(textLeft)
            else:
                file_obj = open(f'{img_idPages}.txt', "a") #a permet d'ajouter du texte sans écraser l'existant
                textLeft, textRight = ExtractText(img,contours1)
                textRightFinal+=textRight+"\n"
                file_obj.write(textLeft)
            file_obj.close()
            img_idPrec = img_idPages
            
def HorizentalExtraction(img_dir, Destinationsave_dir):
    img_idPrec = ""
    for i in img_dir:
        img_id = i.split('\\')[-1] #Enlever le chemin, ne garder que le nom du fichier
        img_idPages = img_id.split('-page')[0] #Ne garder que le nom du cv sans le numero de page
        img = cv2.imread(r'C:/Users/NAWRESS/python/CVIMG/'+img_id)
        grayIMG = gray(img)
        thresh1 = threshold(grayIMG)
        if (not ('_V-' in img_id)): #Dans le cas d'un cv en mode Horizental
            os.chdir(Destinationsave_dir) #Où on va stocker les fichiers.txt (résultat final)
            if img_idPages != img_idPrec :
                file_obj = open(f'{img_idPages}.txt', "w") #w permet de créer le fichier s'il n'existe pas
                text = pytesseract.image_to_string(thresh1, lang='fra+eng')
                file_obj.write(text)
            else:
                file_obj = open(f'{img_idPages}.txt', "a") #a permet d'ajouter du texte sans écraser l'existant
                text = pytesseract.image_to_string(thresh1, lang='fra+eng')
                file_obj.write(text)
            file_obj.close()
            img_idPrec = img_idPages

img_dir = glob('C:/Users/NAWRESS/python/CVIMG/*.jpg')
Destinationsave_dir = Path('C:/Users/NAWRESS/python/ExtractedTextOpenCV')
VerticalExtraction(img_dir, Destinationsave_dir)
HorizentalExtraction(img_dir, Destinationsave_dir)


def drawRectangle(img, contours):
    #Creating a copy of image
    im2 = img.copy()
    #Affichage des contours sur la photo copie im2 using openCV
    text = ""
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        rect = cv2.rectangle(im2, (x,y), (x+w, y+h), (0,255,0), 2)
    return im2

"""Imagesave_dir = Path('C:/Users/NAWRESS/python/ContouredImagesOpenCV')  
for i in img_dir:
    img_id = i.split('\\')[-1]
    img = cv2.imread(r'C:/Users/NAWRESS/python/CVIMG/'+img_id)
    grayIMG = gray(img)
    thresh1 = threshold(grayIMG)
    dilated = dilate(thresh1)
    contours1 = contours(dilated)
    im2 = drawRectangle(img, contours1) 
    os.chdir(Imagesave_dir)
    cv2.imwrite(f'{img_id}.jpg',im2)"""

        