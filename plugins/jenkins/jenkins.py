#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from slackclient import SlackClient
from configparser import ConfigParser
from os import path
import requests

outputs = []

parser = ConfigParser()
parser.read(path.dirname(path.realpath(__file__)) + '/jenkins.conf')

JENKINS_URL = parser.get('jenkins', 'JENKINS_URL')
SLACK_BOT_TOKEN = parser.get('jenkins', 'SLACK_BOT_TOKEN')

# first job job1
JOB_NAME = parser.get('job1', 'JOB_NAME')
JOB_TOKEN = parser.get('job1', 'JOB_TOKEN')
TRIGGER_PHRASE = parser.get('job1', 'TRIGGER_PHRASE')

SLACK_CHANNEL = parser.get('job1', 'SLACK_CHANNEL')
SLACK_USERS = parser.get('job1', 'SLACK_USERS').split()

def process_message(data):
    
    if 'text' in data:
        try:
            text = data['text']
            chan = data['channel']
            user = data['name']
            print(SLACK_USERS)

            if TRIGGER_PHRASE in text and chan == SLACK_CHANNEL:
                sc = SlackClient(SLACK_BOT_TOKEN)
                if user in SLACK_USERS:
                    print(user)
                    print(text)
                    r = requests.get(JENKINS_URL + '/buildByToken/build?job=' + JOB_NAME + '&token=' + JOB_TOKEN)
                    status_code = r.status_code
                    print('status code: ', status_code)
                    print('headers: ', r.headers)
                    
                    output_message = 'Jenkins job "' + JOB_NAME + '" started by ' + user + '\n'
                    output_message += 'Status code: ' + str(status_code)
                    print(sc.api_call("chat.postMessage", as_user="false", icon_emoji=":bowtie:", channel=chan, text=output_message))
                    #outputs.append([data['channel'], output_message])
                else:
                    output_message = 'Sorry, but user "' + user + '" doesn\'t have permission for this job :('
                    print(sc.api_call("chat.postMessage", as_user="false", icon_emoji=":trollface:", channel=chan, text=output_message))
                    #outputs.append([data['channel'], 'Sorry, but user "' + user + '" doesn\'t have permission for this job :('])
                del sc
                
        except KeyError:
            print('KeyError Exception')

