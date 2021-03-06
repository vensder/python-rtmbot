#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.client
from configparser import ConfigParser
from urllib.parse import urlencode
from os import path

parser = ConfigParser()
parser.read(path.dirname(path.realpath(__file__)) + '/telegram.conf')

token = parser.get('bot', 'token')
telegram_chat = parser.get('user', 'telegram-id')
slack_user = parser.get('user', 'slack-id')
slack_name = parser.get('user', 'slack-name')


def send_to_telegram(text):
    
    global token, telegram_chat
    
    conn = http.client.HTTPSConnection("api.telegram.org")
    conn.request('GET', '/' + token + '/sendMessage?' + urlencode({'text': text}) + '&chat_id=' + telegram_chat)

    r1 = conn.getresponse()
    print('telegram response: ', r1.status, r1.reason)


def process_message(data):

    global slack_user, slack_name
    
    if 'text' in data and data['text']:
        try:
            text = data['text']
#            channel = data['channel']
#            user = data['user'] #TODO add 'sent from <user>'
            
            if slack_user in text:
                send_to_telegram(text.replace(slack_user, slack_name))

        except KeyError:
            print('KeyError Exception')
