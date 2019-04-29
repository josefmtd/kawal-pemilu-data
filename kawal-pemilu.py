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
            if len(dummyData['parentIds']) == 4:
                dataTpsDaerah.append(dummyData)
        return dataTpsDaerah
    
    def getKawalPemiluDataSuaraTpsPerDaerah(dataTPSDaerah):
        dataTps = []
        for y in range(len(dataTPSDaerah)):
            dataName = dataTPSDaerah[y]['name']
            data = dataTPSDaerah[y]['data']
            #dataTps.append(dataName)
            #print(dataTps)
            for x in range(len(data)):
                dataTps.append([str(dataTPSDaerah[y]['parentNames'][1]+" " +dataName + str(x+1)),data[str(x+1)]['sum']['pas1'], data[str(x+1)]['sum']['pas2']])
        return dataTps



#usage

testData = KawalPemilu.getDataTPSDaerah(10)

data = KawalPemilu.getKawalPemiluDataSuaraTpsPerDaerah(testData)
