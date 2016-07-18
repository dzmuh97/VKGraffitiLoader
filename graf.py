import requests
import sys
import time

TOKEN = 'ТОКЕН с docs,messages,offline' #asd7a6f78sd78fsd7v678dcf67s8z6c7s89g7sd98f678a6df7ats56d4asd2as45f5a
MYID = 'ID страницы' #473589345

def request(method, params):
	global DATA
	url = 'https://api.vk.com/method/' + method
	params.update({'access_token': TOKEN, 'v': '5.52'})
	print('[REQUEST] Make request..')
	while True:
		try:
			br = requests.post(url, data=params, timeout=15)
			if br.ok:
				data = br.json()
				if 'error' in data:
					if data['error']['error_code'] == 6:
						time.sleep(2)
						continue
					else:
						print('[REQUEST] Error:', data)
						break
				else:
					print('[REQUEST] OK')
					break
		except Exception as e:
			print('[REQUEST] Exception:', e)
			time.sleep(1)
	return data

def load_image(path):
	resp = request('docs.getUploadServer', {'type': 'graffiti'})
	try:
		if 'response' in resp:
			url = resp['response']['upload_url']
		else:
			return ''
	except:
		return ''
	files = {'file': open(path, 'rb')}
	try:
		r = requests.post(url, files=files)
		if r.ok:
			fil = r.json()['file']
		else:
			return ''
	except:
		return ''
	try:
		save = request('docs.save', {'file': fil})['response'][0]['id']
	except:
		save = ''
	return 'doc' + MYID + '_' + str(save)

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print('Нужно указать 2 параметра:\ngraf.py путь_к_вайлу_png id_беседы\ngraf.py test.png 123')
		exit()
	doc = load_image(sys.argv[1])
	request('messages.send', {'chat_id': sys.argv[2], 'attachment': doc})
