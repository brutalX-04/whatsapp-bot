from neonize.proto.waE2E.WAWebProtobufsE2E_pb2 import (
    Message,
    FutureProofMessage,
    InteractiveMessage,
    MessageContextInfo,
    DeviceListMetadata
)
import os, ffmpeg
from . import ( tiktok,
	instagram,
	pinterest,
	bing_image,
	ss_web
)


class rebuild:
	def mp3(path):
	    try:
	        ffmpeg.input(path).output("data/media/download_rebuild.mp3").run()
	        return "succes"

	    except ffmpeg.Error as e:
	        return "failled"


class send_message:
	def interactive_message(client, chat, body, rows):
	    client.send_message(
	        chat,
	        Message(
	            viewOnceMessage=FutureProofMessage(
	                message=Message(
	                    messageContextInfo=MessageContextInfo(
	                        deviceListMetadata=DeviceListMetadata(),
	                        deviceListMetadataVersion=2,
	                    ),
	                    interactiveMessage=InteractiveMessage(
	                        body=InteractiveMessage.Body(text=body),
	                        footer=InteractiveMessage.Footer(text="@brutalx-04"),
	                        header=InteractiveMessage.Header(
	                            title="Message url detected",
	                            hasMediaAttachment=False,
	                        ),
	                        nativeFlowMessage=InteractiveMessage.NativeFlowMessage(
	                            buttons=[
	                                InteractiveMessage.NativeFlowMessage.NativeFlowButton(
	                                    name="single_select",
	                                    buttonParamsJSON='{"title":"List Buttons","sections":[{"title":"convert url to media","rows":%s}]}}'%(rows),
	                                ),
	                            ]
	                        ),
	                    ),
	                )
	            )
	        )
	    )

	def carousel(client, chat, body, footer, cards):
		client.send_message(
	        chat,
	        Message(
	            viewOnceMessage=FutureProofMessage(
	                message=Message(
	                    messageContextInfo=MessageContextInfo(
	                        deviceListMetadata=DeviceListMetadata(), 
	                        deviceListMetadataVersion=2
	                    ), 
	                    interactiveMessage=InteractiveMessage(
	                        body=InteractiveMessage.Body(text=body),
	                        footer=InteractiveMessage.Footer(text=footer),
	                        carouselMessage=InteractiveMessage.CarouselMessage(
	                            cards=cards
	                        )
	                    )
	                )
	            )
	        )
	    )


class media:
	def download_mp4(client, chat, message, text):
		typ, url = text.split(" ")
		if typ == ".mp4_tik":
			tiktok.download(client, chat, message, url, "video")
		elif typ == ".mp4_ig":
			instagram.download(client, chat, message, url, "video")

	def download_mp3(client, chat, message, text):
		typ, url = text.split(" ")
		if typ == ".audio_tik":
			tiktok.download(client, chat, message, url, "audio")
		elif typ == ".ptt_tik":
			tiktok.download(client, chat, message, url, "ptt")
		elif typ == ".audio_ig":
			instagram.download(client, chat, message, url, "audio")
		elif typ == ".ptt_ig":
			instagram.download(client, chat, message, url, "ptt")

	def download_image(client, chat, message, text):
		typ, url = text.split(" ")
		if typ == ".img_ig":
			instagram.download(client, chat, message, url, "image")
		elif typ == ".ss_web":
			if "https://" in url or "http://" in url:
				ss_web.download(client, chat, message, url)
			else:
				client.reply_message("url https:// or http:// required", message)


class scraper:
	def pinterest(client, chat, message, keywords):
		pinterest.get_first_image(client, chat, message, keywords)
	def bing(client, chat, message, keywords):
		bing_image.get(client, chat, message, keywords)
