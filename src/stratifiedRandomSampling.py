""" StratifiedRandomSampling.py
Created on Sat May  23 10:45:12 2019

@author: JosefMTD
"""

import os
import matplotlib

matplotlib.use('Agg')

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import random
import urllib.request
import json
import math

class StratifiedRandomSampling:
    def __init__(self, directory, jumlahSampel):
        self.sampleSize = jumlahSampel
        self.populasiTPS = 814238
        self.directory = directory
        self.nolSatuQuickCount = 0
        self.nolDuaQuickCount = 0
        self.totalSuaraQuickCount = 0
        self.varianceQuickCount = 0
        self.jumlahTPS = {}
        self.dataQuickCount = {}

    def getJumlahTPS(self):
        readURL = urllib.request.urlopen('https://kawal-c1.appspot.com/api/c/0')
        data = json.loads(readURL.read())
        for x in range(len(data['children'])):
            self.jumlahTPS.update( {data['children'][x][1] : data['children'][x][2]} )

    def getSampleData(self, seed):
        self.getJumlahTPS()
        quickCountData = []
        for filename in os.listdir(self.directory):
            if filename.endswith(".csv"):
                dataName = filename[:-4]
                if dataName is not "Luar Negeri":
                    df = pd.read_csv(self.directory+filename)
                    stratumSample = math.ceil(self.jumlahTPS[dataName]/self.populasiTPS*self.sampleSize)
                    sample = df.sample(stratumSample, random_state = seed)
                    self.dataQuickCount.update( {dataName : sample} )
                    #sample.to_csv(self.directory + 'sample/stratifiedRandomSampling/' + filename)
                    self.nolSatuQuickCount += int(np.sum(sample['Suara 01'])*self.jumlahTPS[dataName]/stratumSample)
                    self.nolDuaQuickCount += int(np.sum(sample['Suara 02'])*self.jumlahTPS[dataName]/stratumSample)
                    self.totalSuaraQuickCount += int(np.sum(np.add(sample['Suara 01'], sample['Suara 02']))*self.jumlahTPS[dataName]/stratumSample)
                    quickCountData.append(sample)
                else:
                    continue
            else:
                continue
        self.quickCountData = pd.concat(quickCountData)
        proporsiNolSatu = self.nolSatuQuickCount/self.totalSuaraQuickCount
        proporsiNolDua = self.nolDuaQuickCount/self.totalSuaraQuickCount
        print("Persentase 01: " + str(proporsiNolSatu*100))
        print("Persentase 02: " + str(proporsiNolDua*100))

        for namaProvinsi in self.jumlahTPS.keys():
            jumlahPopulasi = self.jumlahTPS[namaProvinsi]
            sampelNolSatu = self.dataQuickCount[namaProvinsi]['Suara 01'].tolist()
            sampelNolDua = self.dataQuickCount[namaProvinsi]['Suara 02'].tolist()
            sampelTotalSuara = np.add(sampelNolSatu,sampelNolDua).tolist()
            jumlahSampel = len(sampelTotalSuara)
            varianceStratum = self.getVarianceStratum(proporsiNolSatu,sampelNolSatu,sampelTotalSuara,jumlahSampel)
            self.varianceQuickCount += varianceStratum*jumlahPopulasi*(jumlahPopulasi-jumlahSampel)/(jumlahSampel*self.totalSuaraQuickCount*self.totalSuaraQuickCount)

        moe = np.sqrt(self.varianceQuickCount)*100*2.58
        print("Margin of Error: " + str(moe))
        self.quickCountData.to_csv(self.directory + 'sample/[Sample' + str(self.sampleSize) + '][Seed'+ str(seed) +']MOE%.2f'%(moe) + 'NolSatu%.2f'%(proporsiNolSatu*100) + 'NolDua%.2f'%(proporsiNolDua*100) + '.csv', index=False)

    def getVarianceStratum(self, proporsiNolSatu, sampleNolSatu, sampleTotalSuara, jumlahSample):
        vhi = np.subtract(sampleNolSatu, np.multiply(proporsiNolSatu, sampleTotalSuara))
        vh = np.sum(vhi)/jumlahSample
        variance = np.sum(np.square(vhi-vh))/(jumlahSample-1)
        return variance

def main():
	sampelDuaRibu = StratifiedRandomSampling('C:/Users/JosefStevanus/Documents/GitHub/kawal-pemilu-data/csv/', 2000)
	for x in range(10):
		sampelDuaRibu.getSampleData(x)
		
	sampelSeribu = StratifiedRandomSampling('C:/Users/JosefStevanus/Documents/GitHub/kawal-pemilu-data/csv/', 1000)
	for x in range(10):
		sampelSeribu.getSampleData(x)

main()