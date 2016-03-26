#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import gmtime, strftime

# outpust format:
# ['<channel name>', 'text message', 'bot name', 'emoji' ]]

outputs = []

def canary():
    #NOTE: you must add a real channel ID for this to work
#    localtime = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    localtime = strftime("%a, %d %b %Y %H:%M", gmtime())
    outputs.append(["bots", "Bot started at time: " + str(localtime), 'Canary', ':robot_face:'])

canary()
