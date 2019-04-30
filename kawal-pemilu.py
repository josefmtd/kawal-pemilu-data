import urllib.request
import json
import time

class KawalPemilu:
    def __init__(self):
        self.timeNow = time.time()*1000
        self.idTPS = []
        self.nolSatu = []
        self.nolDua = []
        self.suaraSah = []

    def getKawalPemiluJSON(self,id):
        urlAPI = "http://kawal-c1.appspot.com/api/c/" + str(id) + "?" + str(self.timeNow)
        readURL = urllib.request.urlopen(urlAPI)
        data = json.loads(readURL.read())
        return data 

    def getKecamatanData(self,id):
        dataKecamatan = self.getKawalPemiluJSON(id)
        if dataKecamatan['depth'] == 3:
            listKelurahan = self.getChildrenID(dataKecamatan['children'])
            for kelurahan in listKelurahan:
                self.getKelurahanData(kelurahan)
        elif dataKecamatan is None:
            print("Error: ID tidak ada")
        else:
            print("Error: ID bukan Kecamatan")

    def getChildrenID(self,parentChildren):
        listChildren = []
        for x in parentChildren:
            listChildren.append(x[0])
        return listChildren

    def getKelurahanData(self,id):
        dataKelurahan = self.getKawalPemiluJSON(id)
        if dataKelurahan['depth'] == 4:
            #print("Ada", str(len(dataKelurahan['children'])), "TPS di Kelurahan ini")
            listTPS = self.getChildrenID(dataKelurahan['children'])
            for tps in listTPS:
                print("TPS", tps)
                print(dataKelurahan['data'][str(tps)]['sum'])
        elif dataKelurahan is None:
            print("Error: ID tidak ada")
        else:
            print("Error: ID bukan Kelurahan")

    def getDataTPSDaerah(totalTPS):
        dataTpsDaerah = []
        for x in range(totalTPS):
            idTPS = x
            dataNow = KawalPemilu()
            dummyData = dataNow.getKawalPemiluJSON(idTPS)
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
