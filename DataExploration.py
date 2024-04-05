# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 15:58:12 2023

@author: NAWRESS
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Correlation for vertical CV
df = pd.read_csv("C:/Users/NAWRESS/python/ImageData/example_AF_Soulaima_aissa-page1.tsv", engine='python', sep='\t')
df1 = pd.read_csv("C:/Users/NAWRESS/python/ImageData/example_Ahmed Zouaoui-page1.tsv", engine='python', sep='\t')
df = df.drop(df.columns[[0]], axis=1)
df1 = df1.drop(df1.columns[[0]], axis=1)
print("Shape of data : " , df.shape,"\n")
print("La liste des colonnes: ", df.columns.tolist())
print(df.head()) #Affichage des 5 premières lignes
print(df.dtypes) #Les colonnes sont toutes de types float64
print(df.isna().sum())

corr = df.corr()
plt.figure(figsize=(25, 20))
sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns, linewidths=.6, cmap= 'coolwarm', linewidth=1, linecolor='black', annot=True)

corr = df1.corr()
plt.figure(figsize=(25, 20))
sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns, linewidths=.6, cmap= 'coolwarm', linewidth=1, linecolor='black', annot=True)