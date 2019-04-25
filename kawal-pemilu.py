import urllib.request
import json
import time

url = "http://kawal-c1.appspot.com/api/c/0?" + str(int(time.time()*1000))

print(url)

with urllib.request.urlopen(url) as link:
	data = json.loads(link.read().decode())
	print(data)
