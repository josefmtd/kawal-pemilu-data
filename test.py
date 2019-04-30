# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 08:54:04 2019

@author: JosefStevanus
"""

tic = time.clock()
dataKebayoranBaru = KawalPemilu()
dataKebayoranBaru.getKecamatanData(26034)
toc = time.clock()

print(toc-tic)