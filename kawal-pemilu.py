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

idTPS = 1
dataNow = KawalPemilu()
waktuNow = int(time.time()*1000)

print(dataNow.getKawalPemiluJSON(idTPS, waktuNow))
