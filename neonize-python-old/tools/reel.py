import re, requests
from tools import get_env


def download_reel(ids, typ):
	try:
		cookie = get_env.get_value("IG_COOKIE")
		get    = requests.get("https://www.instagram.com/p/%s/?__a=1&__d=dis"%(ids), cookies={ "cookie": cookie }).text
		
		if typ == ".mp4":
			body = re.search('video_versions":\[(.*?)\]', get).group(1)
			url  = re.search('"url":"(.*?)"', body).group(1)

			down = requests.get(url)
			with open('./media/reel.mp4', 'wb') as file:
				file.write(down.content)

			return 'Succes download mp4'

		elif typ == ".mp3" or typ == ".ptt":
			body = re.search('"original_sound_info":{(.*?)}', get).group(1)
			url  = re.search('"progressive_download_url":"(.*?)"', body).group(1)

			down = requests.get(url)
			with open('./media/reel.mp3', 'wb') as file:
				file.write(down.content)

			return 'Succes download mp3'

	except Exception as e:
		return 'Failled'

