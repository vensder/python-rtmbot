#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#russian_roulette.py

'''
def process_message(data):
    
    if 'text' in data:
        try:
            text = data['text']
            channel = data['channel']
            
            if 'russian roulette' in text:
                outputs.append([data['channel'], '<@' + data['user'] + '>--'])
                outputs.append([data['channel'], '@pizza++'])
                #outputs.append(["bots", "<@U0DEX55DL>, bot started at time: " + str(localtime)])

        except KeyError:
            print('KeyError Exception')
'''

from slackclient import SlackClient
from configparser import ConfigParser
import os

parser = ConfigParser()
parser.read(os.path.dirname(os.path.realpath(__file__)) + '/russian_roulette.conf')

token = parser.get('slack', 'top-secret-user-token')

sc = SlackClient(token)
chan = 'C0QN2S8J3'
greeting = '<@U0QLT7CDS>: ++'
print(sc.api_call("chat.postMessage", as_user="true:", channel=chan, text=greeting))
