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
            listKelurahan = self.getKelurahanID(dataKecamatan['children'])
            for kelurahan in listKelurahan:
                self.getKelurahanData(kelurahan)
        elif dataKecamatan is None:
            print("Error: ID tidak ada")
        else:
            print("Error: ID bukan Kecamatan")

    def getKelurahanID(self,kecamatanDataChildren):
        listKelurahan = []
        for x in kecamatanDataChildren:
            listKelurahan.append(x[0])
        return listKelurahan

    def getKelurahanData(self,id):
        dataKelurahan = self.getKawalPemiluJSON(id)
        if dataKelurahan['depth'] == 4:
            print(dataKelurahan['children'])
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
