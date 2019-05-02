# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 08:54:04 2019

@author: JosefStevanus
"""

import pandas

tic = time.clock()
dataJakarta = KawalPemilu()
dataJakarta.getProvinsiData(25823)
toc = time.clock()

df = pandas.DataFrame({'Nama TPS' : dataJakarta.namaTPS, 'ID Kelurahan' : dataJakarta.idKelurahanTPS, 'Suara 01' : dataJakarta.nolSatu, 'Suara 02' : dataJakarta.nolDua, 'Suara Sah' : dataJakarta.suaraSah})

export_csv = df.to_csv (r'C:\Users\JosefStevanus\Documents\GitHub\kawal-pemilu-data\jakarta.csv', index = None, header=True)

print(toc-tic)