# -*- coding: utf-8 -*-
"""
Created on Sun May  7 19:16:27 2023

@author: NAWRESS
"""
import os
from pathlib import Path
from glob import glob
import nltk
from nltk.stem import WordNetLemmatizer 
import simplemma
from nltk.corpus import stopwords

cvsPath = 'C:/Users/NAWRESS/python/ExtractedText'
CVs_dirTesseract = Path('C:/Users/NAWRESS/python/ExtractedText')
CVs_dirOpenCV = Path('C:/Users/NAWRESS/python/ExtractedTextOpenCV')

def CountAlphanumeric(line):
    count = 0
    for caractere in line:
        if (caractere.isalnum()):
            count+=1      
    return count
    
def removeUselessLines(lines):

    for line in lines:
        if(line == "\n"):
            lines.remove(line)
        else:
            line1 = line.strip()
            if (len(line1)<=2 or CountAlphanumeric(line1)<2):
                lines.remove(line)     
    res = " ".join([item for item in lines])
    return(res)
   
def CorrectWrongDetection(text):
    text = text.replace(" e ","\n- ")
    text = text.replace(" = ","\n- ")
    text = text.replace(" œ "," - ")
    text = text.lower()
    return text

def lemmatize_ligne(line):
    wnl = WordNetLemmatizer()
    lemmatizer_sentence = []  
    tokenizer=nltk.tokenize.WhitespaceTokenizer()
    for word in tokenizer.tokenize(line):
        lemmatizer_sentence.append(simplemma.lemmatize(word, lang='fr'))
        lemmatizer_sentence.append(" ")
    return("".join(lemmatizer_sentence))

def removeStopWordsFromLine(line):
    final_stopwords_list = stopwords.words('english') + stopwords.words('french')
    NotStopWords=[]
    wnl = WordNetLemmatizer()
    lemmatizer_sentence = []  
    tokenizer=nltk.tokenize.WhitespaceTokenizer()
    for word in tokenizer.tokenize(line):
        if not word in final_stopwords_list:
            NotStopWords.append(word)
            NotStopWords.append(" ")
    return("".join(NotStopWords))

def lemmetizeText(TextLines):
    FinalSentences = [] 
    for line in TextLines:
        NewLine = lemmatize_ligne(line)
        NewLine2 = removeStopWordsFromLine(NewLine)
        FinalSentences.append(NewLine2 + "\n")
    return(FinalSentences)

               
def nettoyage(CVs_dir):
    os.chdir(CVs_dir)
    CVdirr = glob(r'*.txt')
    for i in CVdirr:
        file_obj = open(f'{i}', "r")
        lines = file_obj.readlines()
        file_obj.close()
        lemmetized = lemmetizeText(lines)
        UselessLremoved= removeUselessLines(lemmetized)
        corrected = CorrectWrongDetection(UselessLremoved)
        file_obj = open(f'{i}', "w")
        file_obj.write(corrected)
        file_obj.close()
    
#nettoyage(CVs_dirTesseract)
nettoyage(CVs_dirOpenCV)