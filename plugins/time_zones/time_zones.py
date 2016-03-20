#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import arrow
from datetime import datetime
from configparser import ConfigParser
import os
#from pytz import timezone

outputs = []

parser = ConfigParser()
parser.read(os.path.dirname(os.path.realpath(__file__)) + '/time_zones.conf')

# set default Time Zone
tz = parser.get('time_zones', 'default')
# get set of Time Zones from config file
timezone_set = set(parser.get('time_zones', 'set').split())

def time_parsing(user_string,tz):
    for word in user_string.split():
        if ':' in (word):
            hhmm = word.split(':')
            if len(hhmm) == 2:
                hh, mm = hhmm
                if hh.isnumeric() and mm.isnumeric():
                    hh = int(hh)
                    mm = int(mm)
                    if hh <= 24 and mm <= 60:
                        return(word)
    
    return(arrow.now(tz).format('HH:mm'))

def process_message(data):
    
    global tz
    global timezone_set
    
    if 'text' in data:
        try:
            text = data['text']
            channel = data['channel']

            if '@time' in text:
                if 'tz' in data:
                    tz = data['tz'] # get user's timezone from slack
                timezone_user = {tz} # convert user's timezone to set'
                timezonelist = list(timezone_set | timezone_user) # add user's timezone to set of main Time Zones'
                timezonelist.sort() # sort list of time zones
                time_string = time_parsing(text, tz)
                #print(time_string)
                
                local_time = arrow.get(datetime.now(), tz)
                string_time = local_time.format('YYYY-MM-DD') + ' ' + time_string + local_time.format(':ss ZZ')
                my_time = arrow.get(string_time, 'YYYY-MM-DD HH:mm:ss ZZ')
                #print(type(my_time))

                output_message = ''
                for zone in timezonelist:
                    zone_time = my_time.to(zone)
                    hhmm_time = zone_time.format('HH:mm')
                    your_tz = ''
                    if zone == tz:
                        your_tz = ' <- Your timezone'
                    output_message += hhmm_time + ' (' + zone + ')' + your_tz + '\n'
                
                outputs.append([data['channel'], output_message])

        except KeyError:
            print('KeyError Exception')



