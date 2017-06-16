import json as j
import requests as r
from random import randint

def getComic(num):
	url = 'http://xkcd.com/'+num
	data = r.get(url)
	print(data.text)
	parsed = j.loads(data.text)
	comicNumber = parsed['num']
	imgURL = parsed['img']
	return imgURL,comicNumber

TOKEN = "273110074:AAG6XZRPX_E9F2m9WFKqNg3tnopilkf5s_Y"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
mytext = '''Bud can you please send "/new" or "/latest" for recent comic and  "/random" or "/more" for others'''

def sendPhoto(chat_id,img):
    r.get(URL+'sendPhoto?chat_id={}&photo={}'.format(chat_id,img))

def sendMessage(chat_id,text):
    r.get(URL+'sendMessage?chat_id={}&text={}'.format(chat_id,text))

def handleRequests(offset):
	url = 'getUpdates'
	if offset:
		url = url +'?offset={}'.format(offset)
	data  = r.get(URL+url)
	updates = j.loads(data.text)
	if len(updates["result"])==0:
		return

	for last_update in updates["result"]:
		print('Handling update of :{}'.format(last_update["update_id"]))
		text = last_update["message"]["text"]
		chat_id = last_update["message"]["chat"]["id"]
		if text == '/latest' or text == '/new':
			img,num = getComic('info.0.json')
			sendPhoto(chat_id,img)
		else:
			if text == '/random' or text == '/more':
				img,num = getComic('info.0.json')
				random = randint(1,num-1)
				img,num = getComic(str(random)+'/info.0.json')
				sendPhoto(chat_id,img)
			else:
				sendMessage(chat_id,mytext)
	offset = updates["result"][-1]["update_id"]+1
	f=open('offset.dat','w')
	f.write(str(offset))
	f.close()

while True:
	offset = None
	try:
		f=open('offset.dat','r')
		offset = int(f.readline())
		f.close()
	except:
		pass
	print('offset is {}'.format(offset))
	handleRequests(offset)
