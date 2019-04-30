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

    def getProvinsiData(self,id):
        dataProvinsi = self.getKawalPemiluJSON(id)
        if dataProvinsi['depth'] == 1:
            listKabupaten = self.getChildrenID(dataProvinsi['children'])
            for kabupaten in listKabupaten:
                self.getKabupatenData(kabupaten)
        elif dataProvinsi is None:
            print("Error: ID tidak ada")
        else:
            print("Error: ID bukan Provinsi")

    def getKabupatenData(self,id):
        dataKabupaten = self.getKawalPemiluJSON(id)
        if dataKabupaten['depth'] == 2:
            listKecamatan = self.getChildrenID(dataKabupaten['children'])
            for kecamatan in listKecamatan:
                self.getKecamatanData(kecamatan)
        elif dataKabupaten is None:
            print("Error: ID tidak ada")
        else:
            print("Error: ID bukan Kabupaten")

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
            print('Nama Kelurahan:', dataKelurahan['name'])
            self.parseTPSData(dataKelurahan['data'],dataKelurahan['name'],listTPS)
        elif dataKelurahan is None:
            print("Error: ID tidak ada")
        else:
            print("Error: ID bukan Kelurahan")

    def parseTPSData(self,dataKelurahan,namaKelurahan,listTPS):
        for x in listTPS:
            try:
                self.idTPS.append(namaKelurahan + str(x))
                self.nolSatu.append(dataKelurahan[str(x)]['sum']['pas1'])
                self.nolDua.append(dataKelurahan[str(x)]['sum']['pas2'])
                self.suaraSah.append(dataKelurahan[str(x)]['sum']['sah'])
            except KeyError:
                continue

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
