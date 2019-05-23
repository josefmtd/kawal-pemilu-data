""" DistributionPlot.py
Created on Thu May 23 10:01:00 2019

@author: JosefMTD
"""

import os
import matplotlib

matplotlib.use('Agg')

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

directory = '/home/josefmtd/kawal-pemilu-data/csv/'
data = {}
cleanNolSatuNasional = []
cleanNolDuaNasional = []
cleanTotalSuaraNasional = []

for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        dataName = filename[:-4]
        data[dataName] = pd.read_csv(directory+filename)

        nolSatu = data[dataName]["Suara 01"]
        nolDua = data[dataName]["Suara 02"]

        cleanNolSatu = []
        cleanNolDua = []

        for x in range(len(nolSatu)):
            if nolSatu[x] == 0 and nolDua[x] == 0:
                continue
            else:
                cleanNolSatu.append(nolSatu[x])
                cleanNolDua.append(nolDua[x])

        cleanTotalSuara = np.add(cleanNolSatu, cleanNolDua)

        cleanNolSatuNasional += cleanNolSatu
        cleanNolDuaNasional += cleanNolDua
        cleanTotalSuaraNasional += cleanTotalSuara.tolist()

        percentageNolSatu = np.divide(cleanNolSatu, cleanTotalSuara)*100
        percentageNolSatuSeries = pd.Series(percentageNolSatu, name = "Distribusi Persentase 01 di " + dataName)

        plotDistribusi, seaborn = plt.subplots()
        sns.distplot(percentageNolSatuSeries, kde=False, bins=100, ax=seaborn)
        plotDistribusi.savefig('../img/distribution/'+dataName+'.png')
        continue
    else:
        continue

percentageNolSatuNasional = np.divide(cleanNolSatuNasional, cleanTotalSuaraNasional)*100
percentageNolSatuNasionalSeries = pd.Series(percentageNolSatuNasional, name = "Distribusi Persentase 01 Nasional")

plotDistribusiNasional, seabornNasional = plt.subplots()
sns.distplot(percentageNolSatuNasionalSeries, kde=False, bins=100, ax=seabornNasional)
plotDistribusiNasional.savefig('../img/distribution/Nasional.png')
