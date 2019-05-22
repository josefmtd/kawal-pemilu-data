import urllib.request
import json
import time

class KawalPemilu:
    def __init__(self):
        self.timeNow = time.time()*1000
        self.nomorTPS = []
        self.linkKP = []
        self.nolSatu = []
        self.nolDua = []
        self.suaraSah = []
        self.namaKelurahan = []

    def getKawalPemiluJSON(self,id):
        urlAPI = "http://kawal-c1.appspot.com/api/c/" + str(id) + "?" + str(self.timeNow)
        readURL = urllib.request.urlopen(urlAPI)
        data = json.loads(readURL.read())
        return data

    def getNationalData(self):
        dataNasional = self.getKawalPemiluJSON(0)
	listProvinsi = self.getChildrenID(dataNasional['children'])
        for provinsi in listProvinsi:
            self.getProvinsiData(provinsi)

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
            listTPS = self.getChildrenID(dataKelurahan['children'])
            self.parseTPSData(dataKelurahan['data'],dataKelurahan['name'], dataKelurahan['parentNames'], listTPS,dataKelurahan['id'])
        elif dataKelurahan is None:
            print("Error: ID tidak ada")
        else:
            print("Error: ID bukan Kelurahan")

    def parseTPSData(self,dataKelurahan,namaKelurahan,namaParent,listTPS,idKelurahan):
        for x in listTPS:
            try:
                self.nolSatu.append(dataKelurahan[str(x)]['sum']['pas1'])
                self.nolDua.append(dataKelurahan[str(x)]['sum']['pas2'])
                self.suaraSah.append(dataKelurahan[str(x)]['sum']['sah'])
		self.namaKelurahan.append(namaKelurahan, ',', namaParent[3], ',', namaParent[2], ',', namaParent[1])
                self.nomorTPS.append(str(x))
                self.linkKP.append('https://kawalpemilu.org#' + str(idKelurahan))
            except KeyError:
                continue
