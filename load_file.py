#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from time import mktime
from time import sleep
import sys
import subprocess
import feedparser
import json
import datetime
import re
from bs4 import BeautifulSoup

BOT_TOKEN = "bot1"
CHAN_ID = "420421676:AAFYUn7967VCOLNBE-HQuTJPF2xElCo8agY"
API_URL = "https://api.telegram.org/bot" + BOT_TOKEN + "/"

def sendMessage (text):
    output = subprocess.check_output(["curl", "-s", "-X", "POST", API_URL + "sendMessage",
            "-F", "chat_id=" + CHAN_ID, "-F", "text="+text,
            "-F", "parse_mode=Markdown", '-F', "disable_web_page_preview=true"]) 
    return output

def sendPhoto (photo):
    output = subprocess.call(["curl", "-s", "-X", "POST", API_URL + "sendPhoto",
            "-F", "chat_id=" + CHAN_ID, "-F", "photo=@"+photo]) 
    return output

def downloadAndSend (url, extension):
    outfile = subprocess.check_output(["mktemp",
        "/tmp/fcomicsXXXXX","--suffix=."+extension]).decode('utf-8')
    outfile = outfile.replace ("\n", "")

    subprocess.call(["curl", "-s", url, "-o", outfile])
    sendPhoto(outfile)
    subprocess.call(["rm", "-v", outfile])


if __name__ == '__main__':
    arg = "" if len(sys.argv) == 1 else sys.argv[1]
    d = feedparser.parse ("http://www.lemonde.fr/rss/une.xml")
    for i in d.entries:
       date = datetime.datetime.fromtimestamp(mktime(i['published_parsed']))
       if date < datetime.datetime.now() - datetime.timedelta(hours=4):
             continue
       link = i['links'][0]['href']
       image = i['links'][1]['href']
       summary = re.sub('<.*$', '', i['summary'])
       title = i['title']
       sendMessage("*"+title+'*\n_' + summary + '_\n[lien](' + link + ')')
       downloadAndSend(image,"jpg")
       sleep (1)

