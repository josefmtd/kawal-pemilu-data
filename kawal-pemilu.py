import urllib.request
import json
import time

class KawalPemilu:
    def __init__(self):
        self.idTPS = []
        self.nolSatu = []
        self.nolDua = []
        self.suaraSah = []

    def getKawalPemiluJSON(self,id,timenow):
        urlAPI = "http://kawal-c1.appspot.com/api/c/" + str(id) + "?" + str(timenow)
        readURL = urllib.request.urlopen(urlAPI)
        data = json.loads(readURL.read())
        return data 
    
    def getDataTPSDaerah(totalTPS):
        dataTpsDaerah = []
        for x in range(totalTPS):
            idTPS = x
            dataNow = KawalPemilu()
            waktuNow = int(time.time()*1000)
            dummyData = dataNow.getKawalPemiluJSON(idTPS, waktuNow)
            print(idTPS)
            if not dummyData:
                continue
            if dummyData['depth'] == 4:
                dataTpsDaerah.append(dummyData)
        return dataTpsDaerah
    
    def getKawalPemiluDataSuaraTpsPerDaerah(dataTPSDaerah):
        dataTps = []
        for y in range(len(dataTPSDaerah)):
            dataName = dataTPSDaerah[y]['name']
            data = dataTPSDaerah[y]['data']
            print(y, dataName, data)
            for x in data:
                if 'pas1' not in data[x]['sum']:
                    continue
                if 'pas2' not in data[x]['sum']:
                    continue
                provinsi = str(dataTPSDaerah[y]['parentNames'][1])
                kabupaten = str(dataTPSDaerah[y]['parentNames'][2])
                wilayah = str(dataTPSDaerah[y]['parentNames'][3])
                daerahTps = str(dataName + " "+ x)
                suaraPas1 = data[x]['sum']['pas1']
                suaraPas2 = data[x]['sum']['pas2']
                dataTps.append([provinsi, kabupaten, wilayah, daerahTps ,suaraPas1, suaraPas2])
        return dataTps
