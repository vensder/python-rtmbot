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
TOKEN = parser.get('staging', 'TOKEN')

JOB_NAME = parser.get('staging', 'NAME')
JOB_TOKEN = parser.get('staging', 'TOKEN')
TRIGGER = parser.get('staging', 'TRIGGER')
SLACK_CHANNEL = parser.get('staging', 'SLACK_CHANNEL')
SLACK_USERS = parser.get('staging', 'SLACK_USERS').split()

trigger_phrase = TRIGGER
# PATTERNS=( '^\w+\.overl\.ai\.coffee' '^\w+\.ehr\.works\.run' '^\w+\.staging\.visitnow.\org' )

def send_request_to_Jenkins(domain, user, channel):
    if user in SLACK_USERS:
        print(user)
        try:
            r = requests.get(JENKINS_URL \
                         + '/buildByToken/buildWithParameters?job=' + JOB_NAME \
                         + '&token=' + JOB_TOKEN \
                         + '&FULLDOMAIN=' + domain \
                         + '&USERNAME=' + user)

            # r = requests.get(JENKINS_URL + '/buildByToken/buildWithParameters?job=' + JOB_NAME + '&token=' + JOB_TOKEN)
            status_code = r.status_code
            print('status code: ', status_code)
            print('headers: ', r.headers)
            output_message = 'Jenkins job "' + JOB_NAME + '" started by ' + user + '\n'
            output_message += 'Status code: ' + str(status_code)
            #print(sc.api_call("chat.postMessage", as_user="false", icon_emoji=":bowtie:", channel=chan,
            #                  text=output_message))
            # outputs.append([data['channel'], output_message])
        except Exception as e:
            output_message = "Oops... happened while we trying to send request to Jenkins:\n"
            output_message += "JENKINS_URL: " + JENKINS_URL + '\n'
            output_message +="JOB_NAME: " + JOB_NAME + '\n'
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

            trigger = re.compile(trigger_phrase)
            if trigger.match(text):
                if channel == SLACK_CHANNEL:
                    string_with_domain = trigger.split(text)[1] # rest of text without trigger phrase
                    print(string_with_domain)
                    mask_overlay = re.compile(r'[\w-]+\.overl\.ai\.coffee') # precompile pattern for <subdomain>.overl.ai.coffee
                    mask_ehr = re.compile(r'[\w-]+\.ehr\.works\.run') # precompile pattern for <subdomain>.ehr.works.run
                    mask_visit = re.compile(r'[\w-]+\.staging\.visitnow\.org') # precompile pattern for <subdomain>.staging.visitnow.org

                    if mask_overlay.search(string_with_domain):
                        search_domain = mask_overlay.search(string_with_domain)
                        domain = search_domain.group()
                        print(domain)
                        send_request_to_Jenkins(domain, user, channel)

                    elif mask_ehr.search(string_with_domain):
                        search_domain = mask_ehr.search(string_with_domain)
                        domain = search_domain.group()
                        print(domain)
                        send_request_to_Jenkins(domain, user, channel)

                    elif mask_visit.search(string_with_domain):
                        search_domain = mask_visit.search(string_with_domain)
                        domain = search_domain.group()
                        print(domain)
                        send_request_to_Jenkins(domain, user,channel)

                    else:
                        mask = re.compile(r'([A-Za-z0-9-]+\.)+\w+')  # domain pattern
                        domain = "<not in pattern>"
                        if mask.search(string_with_domain):
                            search_domain = mask.search(string_with_domain)
                            domain = search_domain.group()
                            print("This domain", domain, "is not valid for staging")
                            outputs.append([channel, "This domain " + domain + " is not valid for staging" ])
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
