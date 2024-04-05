# -*- coding: utf-8 -*-
"""
Created on Mon May  1 11:21:02 2023

@author: NAWRESS
"""
import pytesseract
from pytesseract import Output
import numpy as np
from glob import glob
import os
from pathlib import Path
import cv2
import pandas as pd
import itertools 
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'


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
    details = pytesseract.image_to_data(img, lang='fra+eng' ,output_type=Output.DATAFRAME)
    return details

DatapathSave = 'C:/Users/NAWRESS/python/CvDataFinal'
Destinationsave_dir = Path('C:/Users/NAWRESS/python/ExtractedText')
DatapathSave_dir = Path('C:/Users/NAWRESS/python/CvDataFinal') 
img_dir = glob('C:/Users/NAWRESS/python/CVIMG/*.jpg')

def HorizentalExtraction(img_dir, Destinationsave_dir):
    img_idPrec = ""
    for i in img_dir:
        img_id = i.split('\\')[-1] #Enlever le chemin, ne garder que le nom du fichier
        img_idPages = img_id.split('-page')[0] #Ne garder que le nom du cv sans le numero de page
        img = cv2.imread(r'C:/Users/NAWRESS/python/CVIMG/'+img_id)
        grayIMG = gray(img)
        thresh1 = threshold(grayIMG)
        if (not('_V-' in img_id)): #Dans le cas d'un cv en mode Horizental
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

def VerticalExtractionData(img_dir, Destinationsave_dir):
    img_idPrec = ""
    dfFinal = pd.DataFrame() #initialisation du dataframe de chaque cv
    for i in img_dir:
        img_id = i.split('\\')[-1] #Enlever le chemin, ne garder que le nom du fichier
        img_idPages = img_id.split('-page')[0] #Ne garder que le nom du cv sans le numero de page
        img = cv2.imread(r'C:/Users/NAWRESS/python/CVIMG/'+img_id)
        grayIMG = gray(img)
        thresh1 = threshold(grayIMG)
        if ('_V-' in img_id):
            os.chdir(DatapathSave_dir) #Où on va stocker les fichiers.txt (résultat final)
            details = extractData(thresh1)
            if ((img_idPrec == "" and img_idPages != img_idPrec) or img_idPages == img_idPrec):
                dfFinal = pd.concat([dfFinal, details], ignore_index=True)
            else:
                if not dfFinal.empty: 
                    dfFinal.to_csv(os.path.join(f'{img_idPrec}.tsv'), sep="\t")
                    dfFinal = pd.DataFrame() #Pour réinitialiser le dataframe principal
                    dfFinal = pd.concat([dfFinal, details], ignore_index=True)
            img_idPrec = img_idPages
            
 

def FindLargestEcart(liste):
    LargeEcart = -1
    urlist_len = len(liste)-1
    for i in range(len(liste)-1):
        if (liste[i] != liste[i+1]):
                ecart = liste[i+1] - liste[i]
                if(ecart > LargeEcart):
                    LargeEcart = liste[i+1] - liste[i]
                    xLeft=liste[i]
                    xright=liste[i+1]
    return xLeft, xright

def BuildTextFromDF(df):
    ligneprec = 0
    text_final = ""
    lignePrec=0
    for index, row in df.iterrows():
        ligneActuelle = int(row['line_num'])
        text = str(row['text'])
        conf = row['conf']
        if (conf>60.00):
            if text != 'nan ':
                if (lignePrec != ligneActuelle):
                    text_final+="\n"
                text_final+=text + " "
            lignePrec = ligneActuelle
    return text_final

def FindVerticalLine(tsv_dir):
    tsv_dirr = glob(f'{tsv_dir}/*.tsv')
    for i in tsv_dirr:
        os.chdir(DatapathSave_dir)
        img_id = i.split('\\')[-1] #Enlever le chemin, ne garder que le nom du fichier
        img_idPages = img_id.split('.tsv')[0]
        df = pd.read_csv(f'{i}', engine='python', sep='\t')
        df = df.drop(df.columns[[0]], axis=1)
        pd.set_option('mode.chained_assignment', None) #switch off the warning SettingWithCopyWarning entirely.
        data = df[['left']]
        #data['new_index']=range(len(data))
        #data.set_index(keys='new_index', inplace=True)
        pd.reset_option('mode.chained_assignment')
        ListeAbcisses = np.asarray(data['left'].tolist(), dtype = 'int')
        ListeAbcisses = ListeAbcisses[(ListeAbcisses>np.quantile(ListeAbcisses, 0.1)) & (ListeAbcisses<np.quantile(ListeAbcisses, 0.9))]
        ListeAbcisses = list(dict.fromkeys(ListeAbcisses))
        ListeAbcisses.sort()
        LeftSide, rightSide = FindLargestEcart(ListeAbcisses)
        df['zone']=np.where(df['left']<LeftSide, 0, 1)
        leftZoneblock = df[df['zone']==0]
        rightZoneblock = df[df['zone']==1]
        leftText = BuildTextFromDF(leftZoneblock)
        rightText= BuildTextFromDF(rightZoneblock)
        os.chdir(Destinationsave_dir)
        file_obj = open(f'{img_idPages}.txt', "w") #w permet de créer le fichier s'il n'existe pas
        file_obj.write(leftText + "\n" + rightText)
        file_obj.close()


HorizentalExtraction(img_dir, Destinationsave_dir)
VerticalExtractionData(img_dir, Destinationsave_dir)        
FindVerticalLine(DatapathSave) #Exception Bassem Abdallah






    
        
    