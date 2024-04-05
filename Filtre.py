# -*- coding: utf-8 -*-
"""
Created on Sun May 14 10:35:27 2023

@author: NAWRESS
"""
from pathlib import Path
from glob import glob
import numpy as np
import PyPDF2
import webbrowser

cvPath = "C:/Users/NAWRESS/python/ExtractedText/0_CV_2020-04-30-015905_V.txt"
CVs_dir = Path('C:/Users/NAWRESS/python/ExtractedText')

def FindScoreByCV(cvPath, dict1):
    file_obj = open(f'{cvPath}', "r")
    text = file_obj.read()
    score=0
    for key, value in dict1.items():
        if ((text.find(key))>0):
            score+=value
    return score   

#dict1 = {"gestion d'équipe":2, 'gestion projet':3, "management d'équipe":2}
#dict1 = {'finance':3,'optimisation':3, 'Power BI':1}
#dict3 ={'java':3,'jenkins':1}
dict1 = {'power bi':3}
#FindScoreByCV(cvPath, dict1)


def FindAllScoresTesseract(dict1):
    cv_dir = glob('C:/Users/NAWRESS/python/ExtractedText/*.txt')
    dictScores = {}
    for i in cv_dir:
        nomProfil = i.split('\\')[-1]
        nomProfil = nomProfil.split('.txt')[0]
        #print(FindScoreByCV(i, dict1))
        if ((FindScoreByCV(i, dict1))>0): 
            dictScores[nomProfil]=FindScoreByCV(i, dict1)
    return dictScores

#print(FindAllScoresTesseract(dict1))


def FindAllScoresOpenCV(dict1):
    cv_dir = glob('C:/Users/NAWRESS/python/ExtractedTextOpenCV/*.txt')
    dictScores = {}
    for i in cv_dir:
        nomProfil = i.split('\\')[-1]
        nomProfil = nomProfil.split('.txt')[0]
        #print(FindScoreByCV(i, dict1))
        if ((FindScoreByCV(i, dict1))>0): 
            dictScores[nomProfil]=FindScoreByCV(i, dict1)
    return dictScores

print(FindAllScoresOpenCV(dict1))

def FindAllScores(dict1):
    dictOpenCV = FindAllScoresOpenCV(dict1)
    dictTesseract = FindAllScoresTesseract(dict1)
    dictFinal=dictTesseract
    for key, value in dictOpenCV.items():
        if (key in dictFinal):
            if (value > dictFinal[key]):
                dictFinal[key]=value
        else:
            dictFinal[key]=value
    liste= sorted(dictFinal.items(), key=lambda x:x[1], reverse=True)
    listFinal=[]
    for i in liste:
        listFinal.append(i[0])
    for i in range(len(listFinal)):
        if (listFinal[i][-2:]=='_V'):
            listFinal[i] = (listFinal[i])[:-2]
    return listFinal
    
#FindAllScores(dict3)
#print(FindAllScores(dict1))

def GetPDF(name):
    pdf_dir = glob('C:/Users/NAWRESS/python/CVS/*.pdf')
    for pdf_file in pdf_dir:
        nomProfil = pdf_file.split('\\')[-1]
        nomProfil = nomProfil.split('.pdf')[0]
        if name in pdf_file:
            webbrowser.open(f'{pdf_file}')
        
#GetPDF(FindAllScores(dict3)[3])


        

    