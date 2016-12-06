#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from configparser import ConfigParser
from os import path
import requests

outputs = []

parser = ConfigParser()
parser.read(path.dirname(path.realpath(__file__)) + '/jenkins.cfg')

JENKINS_URL = parser.get('jenkins', 'JENKINS_URL')

JOB_NAME_DEMO = parser.get('demo', 'NAME')
JOB_TOKEN_DEMO = parser.get('demo', 'TOKEN')
TRIGGER_DEMO = parser.get('demo', 'TRIGGER')
SLACK_CHANNEL_DEMO = parser.get('demo', 'SLACK_CHANNEL')
SLACK_USERS_DEMO = parser.get('demo', 'SLACK_USERS').split()

# PATTERNS=( '^\w+\.demo\.ai\.coffee' '^\w+\.demo\.visitnow.\org' )

def send_request_to_Jenkins_demo(domain, user, channel):
    if user in SLACK_USERS_DEMO:
        print(user)
        try:
            r = requests.get(JENKINS_URL \
                             + '/buildByToken/buildWithParameters?job=' + JOB_NAME_DEMO \
                             + '&token=' + JOB_TOKEN_DEMO \
                             + '&FULLDOMAIN=' + domain \
                             + '&USERNAME=' + user)

            # r = requests.get(JENKINS_URL + '/buildByToken/buildWithParameters?job=' + JOB_NAME + '&token=' + JOB_TOKEN)
            status_code = r.status_code
            print('status code: ', status_code)
            print('headers: ', r.headers)
            output_message = "Jenkins job " + JOB_NAME_DEMO + " started by " + user + '\n'
            output_message += "Status code: " + str(status_code)
            outputs.append([channel, output_message])
            #print(sc.api_call("chat.postMessage", as_user="false", icon_emoji=":bowtie:", channel=chan,
            #                  text=output_message))
            # outputs.append([data['channel'], output_message])
        except Exception as e:
            output_message = "Oops... happened while we trying to send request to Jenkins:\n"
            output_message += "JENKINS_URL: " + JENKINS_URL + '\n'
            output_message +="JOB_NAME: " + JOB_NAME_DEMO + '\n'
            output_message +="DOMAIN: " + domain + '\n'
            outputs.append([channel, output_message])
            print('Exception when i trying to send request to Jenkins: ', e)
    else:
        output_message = 'Sorry, but user "' + user + '" doesn\'t have permission for this job :('
        #print(sc.api_call("chat.postMessage", as_user="false", icon_emoji=":trollface:", channel=chan,
        #                  text=output_message))
        outputs.append([channel, 'Sorry, but user "' + user + '" doesn\'t have permission for this job :('])

    # del sc


def process_message(data):

    if 'text' in data and data['text']:
        try:
            text = data['text']
            channel = data['channel']
            user = data['name']

            trigger = re.compile(TRIGGER_DEMO)
            if trigger.match(text):
                if channel == SLACK_CHANNEL_DEMO:
                    string_with_domain = trigger.split(text)[1] # rest of text without trigger phrase
                    print(string_with_domain)
                    mask_demo = re.compile(r'[\w-]+\.demo\.ai\.coffee') # precompile pattern for <subdomain>.demo.ai.coffee
                    mask_visit = re.compile(r'[\w-]+\.demo\.visitnow\.org') # precompile pattern for <subdomain>.demo.visitnow.org

                    if mask_demo.search(string_with_domain):
                        search_domain = mask_demo.search(string_with_domain)
                        domain = search_domain.group()
                        print(domain)
                        send_request_to_Jenkins_demo(domain, user, channel)

                    elif mask_visit.search(string_with_domain):
                        search_domain = mask_visit.search(string_with_domain)
                        domain = search_domain.group()
                        print(domain)
                        send_request_to_Jenkins_demo(domain, user, channel)

                    else:
                        mask = re.compile(r'([A-Za-z0-9-]+\.)+\w+')  # domain pattern
                        domain = "<not in pattern>"
                        if mask.search(string_with_domain):
                            search_domain = mask.search(string_with_domain)
                            domain = search_domain.group()
                            print("This domain", domain, "is not valid for demo")
                            outputs.append([channel, "This domain " + domain + " is not valid for demo" ])
                        else:
                            print("That is not like domain, for ex.: newpractice.over.ai.coffee")
                            outputs.append([channel, "That is not like domain, for ex.: newpractice.over.ai.coffee"])

                    output_string = ''
                    emoji = ':robot_face:'
                    except_emoji = ':exclamation:'
                    bot_name = 'SSL Register'

                    try:
                        output_string += 'strange'
                    except Exception as e:
                        outputs.append([channel, str(e) + '. ' + except_phrase, bot_name, except_emoji])
                        print('Exception when i trying to write to channel about exception: ', e)
                else:
                    outputs.append([channel, "Wrong channel. Try it in #ew-stream"])


        except KeyError as e:
            print('KeyError Exception: ', e)
