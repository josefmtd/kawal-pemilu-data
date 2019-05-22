# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 08:54:04 2019

@author: JosefStevanus
"""

import time
import pandas
import kawalpemilu

tic = time.time()
data = kawalpemilu.KawalPemilu()
data.getProvinsiData(26141) # JawaBarat
toc = time.time()

print(toc-tic)

df = pandas.DataFrame({'Nomor TPS' : data.nomorTPS, 'Nama Kelurahan' : data.namaKelurahan, 'Link KawalPemilu' : data.linkKP, 'Suara 01' : data.nolSatu, 'Suara 02' : data.nolDua, 'Suara Sah' : data.suaraSah})

export_csv = df.to_csv (r'../kawal-pemilu-data/csv/jawaBarat.csv', index = None, header=True)
