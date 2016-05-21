#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from configparser import ConfigParser
from os import path
import requests

outputs = []
jobs_dict = {} # dict of dicts with jobs configs
slack_channels = set()

Config = ConfigParser()
Config.read(path.dirname(path.realpath(__file__)) + '/jenkins.cfg')
JENKINS_URL = Config.get('jenkins', 'JENKINS_URL')

# collect all jobs with configs into one dict
for section in Config.sections():
    if 'job' in section:
        jobs_dict[section] = dict(Config.items(section))

# print(jobs_dict)
print(jobs_dict.keys())
print(jobs_dict.items())

# collect slach channels into set
for job in jobs_dict.keys():
    slack_channels.add(jobs_dict[job]['slack_channel'])
print(slack_channels)

def process_message(data):
    print("jenkins_job0.py: " + str(data))
    if 'text' in data and data['text']:
        try:
            text = data['text']
            channel = data['channel']
            user = data['name']
            print('channel: ', channel)
            print('user: ', user)

            if text.startswith('@jenkins help') and channel in slack_channels:
                emoji = ':question:'
                help_text = ''
                for job in jobs_dict.keys():
                    if channel == jobs_dict[job]['slack_channel']:
                        help_text += '{}: ```{}```\n'.format(jobs_dict[job]['help'], jobs_dict[job]['trigger'])

                outputs.append([channel, help_text, 'Jenkins help', emoji])

                '''
                if user in SLACK_USERS:
                    print(user)
                    print(text)
                    r = requests.get(JENKINS_URL \
                                        + '/buildByToken/buildWithParameters?job=' + JOB_NAME \
                                        + '&token=' + JOB_TOKEN \
                                        + '&DRY_RUN=' + DRY_RUN)
                    
                    #r = requests.get(JENKINS_URL + '/buildByToken/buildWithParameters?job=' + JOB_NAME + '&token=' + JOB_TOKEN)
                    status_code = r.status_code
                    print('status code: ', status_code)
                    print('headers: ', r.headers)
                    
                    output_message = 'Jenkins job "' + JOB_NAME + '" started by ' + user + '\n'
                    output_message += 'DRY RUN: ' + DRY_RUN + '\n'
                    output_message += 'Status code: ' + str(status_code)
                    print(sc.api_call("chat.postMessage", as_user="false", icon_emoji=":bowtie:", channel=channel, text=output_message))
                    #outputs.append([data['channel'], output_message])
                else:
                    output_message = 'Sorry, but user "' + user + '" doesn\'t have permission for this job :('
                    print(sc.api_call("chat.postMessage", as_user="false", icon_emoji=":trollface:", channel=channel, text=output_message))
                    #outputs.append([data['channel'], 'Sorry, but user "' + user + '" doesn\'t have permission for this job :('])
                '''

        except KeyError as e:
            print('KeyError Exception: ', e)

