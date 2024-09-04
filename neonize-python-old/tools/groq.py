import requests, json
from tools import get_env
import random

api_key   = random.choice([get_env.get_value("GROK_APIKEY1"), get_env.get_value("GROK_APIKEY2"), get_env.get_value("GROK_APIKEY3")])
ai_prompt = "Hi, Saya adalah WhatsApp bot yang di rancang oleh brutalX, tugas saya adalah membantu menjawab sebuah pesan"
file      = "data/openai-status.txt"


def chat(msg, typ):
    status = open(file, "r").read()
    if typ == "chat" and "chat-of" in status: return
    if typ == "group" and "group-of" in status: return

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "messages":[
            {
                "role": "system",
                "content": ai_prompt
            },
            {
                "role": "user",
                "content": msg,
            }
        ],
        "model": "llama3-8b-8192"
    }

    post = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data).json()

    return post["choices"][0]["message"]["content"]

def change_status(status, message):
    if message.Info.MessageSource.IsFromMe is True:
        chat, group = open(file, "r").read().split("|")
        if status == "chat-on" or status == "chat-of": open(file, "w").write(status+"|"+group)
        if status == "group-on" or status == "group-of": open(file, "w").write(chat+"|"+status)


def status():
    text = open(file, "r").read()

    return "Ai Status : \n  `" + text + "`"

