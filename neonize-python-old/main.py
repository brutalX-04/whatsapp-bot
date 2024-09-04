import logging
import os
import signal
import sys
import ffmpeg
import subprocess
from datetime import timedelta
from neonize.client import NewClient
from neonize.events import (
    ConnectedEv,
    MessageEv,
    PairStatusEv,
    event,
    ReceiptEv,
    CallOfferEv,
)
from neonize.types import MessageServerID
from neonize.utils import log
from PIL import Image
from neonize.utils.enum import ReceiptType
from removebg import RemoveBg
from tools import reel, telebot, tiktok, groq, repair, jadwal, get_env

# --> Set
try:
    sys.path.append("/home/ubuntu/botWhatsapp/")
    os.chdir("/home/ubuntu/botWhatsapp/")
except Exception as e:
    pass

sys.path.insert(0, "/home/ubuntu/botWhatsapp/")


def interrupted(*_):
    event.set()


log.setLevel(logging.DEBUG)
signal.signal(signal.SIGINT, interrupted)


client = NewClient("db.sqlite3")


@client.event(ConnectedEv)
def on_connected(_: NewClient, __: ConnectedEv):
    log.info("⚡ Connected")


@client.event(ReceiptEv)
def on_receipt(_: NewClient, receipt: ReceiptEv):
    log.debug(receipt)


@client.event(CallOfferEv)
def on_call(_: NewClient, call: CallOfferEv):
    log.debug(call)


@client.event(MessageEv)
def on_message(client: NewClient, message: MessageEv):
    handler(client, message)


# --> Send Sticker Build
def send_sticker(client: NewClient, message: MessageEv, chat):
    try:
        client.send_sticker(
            chat,
            "media/download.jpg",
            message,
            "2024",
            "brutalx",
        )
        reaction(chat, message, "✅️")
        os.remove("media/download.jpg")

    except Exception as e:
        reaction(chat, message, "❌️")

# --> Send Image
def send_image(client: NewClient, message: MessageEv, chat, path):
    try:
        client.send_image(
            chat,
            "media/" + path,
            quoted=message,
        )
        reaction(chat, message, "✅️")

    except Exception as e:
        client.reply_message(str(e), quoted=message)
        reaction(chat, message, "❌️")


# --> Send Video
def send_video(client: NewClient, message: MessageEv, chat, path):
    try:
        client.send_video(
            chat,
            "media/" + path,
            quoted=message,
        )
        reaction(chat, message, "✅️")

    except Exception as e:
        reaction(chat, message, "❌️")


# --> Send Audio
def send_audio(client: NewClient, message: MessageEv, chat, typ):
    try:
        client.send_audio(
            chat,
            "media/repair.mp3",
            quoted=message,
            ptt=typ
        )
        reaction(chat, message, "✅️")

    except Exception as e:
        reaction(chat, message, "❌️")


# --> Remove Bg + Send Image
def remove_bg(client: NewClient, message: MessageEv, chat):
    try:
        apikey_rmv = get_env.get_value("REMOVEBG_APIKEY")
        rmbg = RemoveBg(apikey_rmv, "error.log")
        rmbg.remove_background_from_img_file("media/download.jpg")
        send_image(client, message, chat, "download.jpg_no_bg.png")

        os.remove("media/download.jpg_no_bg.png")
        os.remove("media/download.jpg")

    except Exception as e:
        client.reply_message(str(e), quoted=message)
        reaction(chat, message, "❌️")


# --> Read Message
def read(chat, message):
    try:
        client.mark_read(
            message.Info.ID,
            chat=message.Info.MessageSource.Chat,
            sender=message.Info.MessageSource.Sender,
            receipt=ReceiptType.READ,
        ).__str__()
    except:
        pass


# --> Reaction Message
def reaction(chat, message, react):
    client.send_message(
        chat,
        client.build_reaction(
            chat,
            sender=message.Info.MessageSource.Sender,
            message_id=message.Info.ID,
            reaction=react
        ),
    )

def handler(client: NewClient, message: MessageEv):
    #print(message)
    text = message.Message.conversation or message.Message.extendedTextMessage.text
    chat = message.Info.MessageSource.Chat
    user = message.Info.MessageSource.Chat.User

    match text:
        case ".menu":
            read(chat, message)
            client.send_image(
                chat,
                "media/img.jpg",
                caption="[ *`MENU BOT`* ]\n\n> *Delete background* \n    [ *!* ] _send photo or reply message as_ :\n           *.rmv*\n\n> *Img to Sticker* \n    [ *!* ] _send photo or reply message as_ :\n           *.s*\n\n> *Sticker to Img* \n    [ *!* ] _reply sticker as_ :\n           *.i*\n\n> *Reel Ig download*\n    [ *!* ] _send message as_ :\n           *.mp4* _url-reel_\n           *.mp3* _url-reel_\n\n> *Tiktok download*\n    [ *!* ] _send message as_ :\n           *.mp4* _url-video_\n\n> *Groq Ai*\n    [ *!* ] _send message as_ :\n           *.ai* _text_\n\n\n\n [ _Thanks for using_ ]",
                quoted=message,
            )
            return

        case ".s":
            msg = message.Message.extendedTextMessage.contextInfo.quotedMessage
            client.download_any(msg, path="media/download.jpg")
            read(chat, message)
            reaction(chat, message, "⏳")
            send_sticker(client, message, chat)
            return

        case ".rmv":
            msg = message.Message.extendedTextMessage.contextInfo.quotedMessage
            client.download_any(msg, path="media/download.jpg")
            read(chat, message)
            reaction(chat, message, "⏳")
            remove_bg(client, message, chat)
            return

        case ".i":
            try:
                msg = message.Message.extendedTextMessage.contextInfo.quotedMessage
                client.download_any(msg, path="media/download.webp")

                # img = Image.open("media/download.webp").convert("RGB")
                # img.save("media/download.jpg", "jpeg")
                ffmpeg.input("media/download.webp").output("media/download.jpg").run()

                read(chat, message)
                reaction(chat, message, "⏳")
                send_image(client, message, chat, "download.jpg")

                os.remove("media/download.webp")
                os.remove("media/download.jpg")

                return

            except Exception as e:
                client.reply_message(str(e), quoted=message)
                reaction(chat, message, "❌️")

        case ".ai-chat-on":
            groq.change_status("chat-on", message)
            return

        case ".ai-chat-of":
            groq.change_status("chat-of", message)
            return

        case ".ai-group-on":
            groq.change_status("group-on", message)
            return

        case ".ai-group-of":
            groq.change_status("group-of", message)
            return

        case ".ai-status":
            status = groq.status()
            client.reply_message(status, quoted=message)
            return

        case ".off":
            if message.Info.MessageSource.IsFromMe is False: return
            jadwal.offline()
            client.reply_message("owner status set to : `Offline`", quoted=message)
            return

        case ".on":
            if message.Info.MessageSource.IsFromMe is False: return
            jadwal.online()
            client.reply_message("owner status set to : `Online`", quoted=message)
            return

        case ".status":
            if message.Info.MessageSource.IsFromMe is False: return
            msg = "Online" if jadwal.check() is True else "Offline"
            client.reply_message("Owner status : `%s`"%(msg), quoted=message)
            return


    if user == "status":
        try:
            push_name = message.Info.Pushname
            if "imageMessage" in str(message.Message):
                caption = message.Message.imageMessage.caption
                info = "<pre><b>User Info !</b>\nPush Name : <code>%s</code>\nCaption   : <code>%s</code></pre>"%(push_name, caption)
                client.download_any(message.Message, path="media/download.jpg")
                telebot.send_to_telegram("image", info)
                os.remove("media/download.jpg")
                return

            elif "videoMessage" in str(message.Message):
                caption = message.Message.videoMessage.caption
                info = "<pre><b>User Info !</b>\nPush Name : <code>%s</code>\nCaption   : <code>%s</code></pre>"%(push_name, caption)
                client.download_any(message.Message, path="media/download.mp4")
                telebot.send_to_telegram("video", info)
                os.remove("media/download.mp4")
                return
            
            elif "audioMessage" in str(message.Message):
                info = "<pre><b>User Info !</b>\nPush Name : <code>%s</code></pre>"%(push_name)
                client.download_any(message.Message, path="media/download.mp3")
                telebot.send_to_telegram("audio", info)
                os.remove("media/download.mp3")
                return

            elif "extendedTextMessage" in str(message.Message):
                caption = message.Message.extendedTextMessage.text
                info = "<pre><b>User Info !</b>\nPush Name : <code>%s</code>\nCaption   : <code>%s</code></pre>"%(push_name, caption)
                telebot.send_to_telegram("text", info)
                return


        except Exception as e:
            pass


    if "$ " in text:
        msg = text.split(" ")
        command = msg[1]
        if message.Info.MessageSource.IsFromMe is True:
            try:
                if command == "nano" or command == "cat" or command == "vim":
                    output = subprocess.check_output(["cat", msg[2]])
                    decode_output = output.decode("utf-8")
                    client.reply_message(decode_output, quoted=message)
                
                elif len(msg) > 2 and len(msg) < 4:
                    output = subprocess.check_output([msg[1], msg[2]])
                    decode_output = output.decode("utf-8")
                    client.reply_message(decode_output, quoted=message)

                else:
                    output = subprocess.check_output(command, shell=True)
                    decode_output = output.decode("utf-8")
                    client.reply_message(decode_output, quoted=message)
            except:
                reaction(chat, message, "❌️")

        else:
            client.reply_message("`Sory your command acces denied !`", quoted=message)
        
        return


    elif ".ai " in text:
        typ     = "group" if message.Info.MessageSource.IsGroup is True else "chat"
        answer  = text.split(".ai ")[1]
        msg_ai  = groq.chat(answer, typ)

        if msg_ai is not None:
            read(chat, message)
            client.reply_message(msg_ai, quoted=message)
            read(chat, message)

        return


    elif "instagram.com/" in text:
        if ".mp4" in text or ".mp3" in text or ".ptt" in text:
            read(chat, message)
            reaction(chat, message, "⏳")
            ids  = text.split("/")[4]
            typ  = text.split(" ")[0]
            down = reel.download_reel(ids, typ)

            if down == "Succes download mp4":
                send_video(client, message, chat, "reel.mp4")
                os.remove("media/reel.mp4")

            elif down == "Succes download mp3":
                rep = repair.mp3("media/reel.mp3")

                if "Succes." in rep:
                    if ".mp3" in text:
                        send_audio(client, message, chat, False)
                    elif ".ptt" in text:
                        send_audio(client, message, chat, True)

                    os.remove("media/repair.mp3")

                elif"Failled." in rep:
                    reaction(chat, message, "❌️")

                os.remove("media/reel.mp3")

            elif down == "Failled":
                reaction(chat, message, "❌️")

            return

    elif "tiktok.com" in text:
        if ".mp4" in text or ".mp3" in text:
            read(chat, message)
            reaction(chat, message, "⏳")
            typ, url  = text.split(" ")

            if typ == ".mp4":
                down = tiktok.video(url)

            if down == "Succes download mp4":
                send_video(client, message, chat, "download.mp4")
                os.remove("media/download.mp4")
                

            elif down == "Failled":
                reaction(chat, message, "❌️")

            return


    if "imageMessage" in str(message.Message):
        try:
            client.download_any(message.Message, path="media/download.jpg")

            if "True" in str(message.Message.imageMessage.viewOnce):
                read(chat, message)
                reaction(chat, message, "⏳")
                client.send_image(
                    chat,
                    "media/download.jpg",
                    caption="Eitsss",
                    quoted=message,
                )
                reaction(chat, message, "🔥")
                os.remove("media/download.jpg")

            else:
                caption = message.Message.imageMessage.caption

                try:
                    if ".s" in caption:
                        read(chat, message)
                        reaction(chat, message, "⏳")
                        send_sticker(client, message, chat)

                    elif ".rmv" in caption:
                        read(chat, message)
                        reaction(chat, message, "⏳")
                        remove_bg(client, message, chat)
                except:
                    reaction(chat, message, "❌️")

            return

        except Exception as e:
            pass


    else:
        if jadwal.check() is True: return
        if message.Info.MessageSource.IsFromMe is True: return
        read(chat, message)
        client.reply_message("_owner sedang offline, mohon hubungi lain kali_ \n\n`#brutalx_bot`", quoted=message)
        return


@client.event(PairStatusEv)
def PairStatusMessage(_: NewClient, message: PairStatusEv):
    log.info(f"logged as {message.ID.User}")


client.connect()
