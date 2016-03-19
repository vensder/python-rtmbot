#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#russian_roulette.py

from slackclient import SlackClient
from configparser import ConfigParser
import os
from random import choice

parser = ConfigParser()
parser.read(os.path.dirname(os.path.realpath(__file__)) + '/russian_roulette.conf')
token = parser.get('slack', 'top-secret-user-token')

def process_message(data):
    
    if 'text' in data:
        try:
            text = data['text']
            channel = data['channel']

            if 'russian roulette' in text:
                sc = SlackClient(token)
                chan = data['channel']
                shot = '<@' + data['user'] + '>' + choice(['++','--'])
                print(sc.api_call("chat.postMessage", as_user="true:", channel=chan, text=shot))
                del sc

        except KeyError:
            print('KeyError Exception')
