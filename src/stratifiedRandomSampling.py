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

    def getJumlahTPS(self):
        readURL = urllib.request.urlopen('https://kawal-c1.appspot.com/api/c/0')
        data = json.loads(readURL.read())
        for x in range(len(data['children'])):
            self.jumlahTPS.update( {data['children'][x][1] : data['children'][x][2]} )

    def getSampleData(self):
        self.getJumlahTPS()
        quickCountData = []
        for filename in os.listdir(self.directory):
            if filename.endswith(".csv"):
                dataName = filename[:-4]
                if dataName is not "Luar Negeri":
                    df = pd.read_csv(self.directory+filename)
                    sample = df.sample(math.ceil(self.jumlahTPS[dataName]/self.populasiTPS*self.sampleSize))
                    quickCountData.append(sample)
                else:
                    continue
            else:
                continue
        self.quickCountData = pd.concat(quickCountData)
        self.quickCountData.to_csv(self.directory + 'sample/stratifiedRandomSampling.csv')

    def getVariance(self, proporsi):
        vhi = np.subtract(self.sampleNolSatu, np.multiply(proporsi, self.sampleTotalSuara))
        vh = np.sum(vhi)/self.sampleSize
        variance = np.sum(np.square(vhi-vh))/(self.sampleSize-1)
        varianceQuickCount = variance*self.totalTPS*(self.totalTPS-self.sampleSize)/self.sampleSize
        return varianceQuickCount
