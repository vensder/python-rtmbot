#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from configparser import ConfigParser
from os import path
import requests

parser = ConfigParser()
parser.read(path.dirname(path.realpath(__file__)) + '/jenkins.conf')

JENKINS_URL = parser.get('jenkins', 'JENKINS_URL')


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
            channel = data['channel']
            user = data['name']
            print(SLACK_USERS)

            if TRIGGER_PHRASE in text and channel == SLACK_CHANNEL:
                if user in SLACK_USERS:
                    print(user)
                    print(text)
                    r = requests.get(JENKINS_URL + '/buildByToken/build?job=' + JOB_NAME + '&token=' + JOB_TOKEN)
                    status_code = r.status_code
                    print('status code: ', status_code)
                    print('headers: ', r.headers)
                    
                    output_message = 'Jenkins job "' + JOB_NAME + '" started by ' + user + '\n'
                    output_message += 'Status code: ' + str(status_code)
                    
                    outputs.append([data['channel'], output_message])
                else:
                    outputs.append([data['channel'], 'Sorry, but user "' + user + '" doesn\'t have permission for this job :('])
                
        except KeyError:
            print('KeyError Exception')

