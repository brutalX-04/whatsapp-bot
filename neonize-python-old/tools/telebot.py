import requests
from tools import get_env


def send_to_telegram(typ, caption):
	try:
		token, chat_id = get_env.get_value("TELEGRAM_TOKEN"), get_env.get_value("TELEGRAM_CHATID")

		if typ == "image":
			file = open('media/download.jpg', 'rb')
			url  = 'https://api.telegram.org/bot%s/sendPhoto'%(token)
			params = {
				'chat_id': chat_id,
				'caption': caption,
				'parse_mode': 'HTMl'
			}
			file = {
				'photo': file
			}
			requests.post(url, params=params, files=file)

		elif typ == "video":
			file = open('media/download.mp4', 'rb')
			url  = 'https://api.telegram.org/bot%s/sendVideo'%(token)
			params = {
				'chat_id': chat_id,
				'caption': caption,
				'parse_mode': 'HTMl'
			}
			file = {
				'video': file
			}
			requests.post(url, params=params, files=file)
		
		elif typ == "audio":
			file = open('media/download.mp3', 'rb')
			url  = 'https://api.telegram.org/bot%s/sendAudio'%(token)
			params = {
				'chat_id': chat_id,
				'caption': caption,
				'parse_mode': 'HTMl'
			}
			file = {
				'audio': file
			}
			response = requests.post(url, params=params, files=file)
			print(response.text)
		
		elif typ == "text":
			url  = 'https://api.telegram.org/bot%s/sendMessage'%(token)
			params = {
				'chat_id': chat_id,
				'text': caption,
				'parse_mode': 'HTMl'
			}
			requests.post(url, params=params)


	except Exception as e:
		raise e

