#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import arrow
from datetime import datetime
from configparser import ConfigParser
from os import path
#from pytz import timezone

outputs = []

parser = ConfigParser()
parser.read(path.dirname(path.realpath(__file__)) + '/time_zones.conf')

# set default Time Zone
tz = parser.get('time_zones', 'default')
# get set of Time Zones from config file
timezone_set = set(parser.get('time_zones', 'set').split())

def time_parsing(user_string,tz):
    'return time in string, using hh:mm format or hh am (pm)'
    splitted_string = user_string.lower().split()
    
    for word in splitted_string: # for hh:mm format (12:23)
        if ':' in (word):
            hhmm = word.split(':')
            if len(hhmm) == 2:
                hh, mm = hhmm
                if hh.isnumeric() and mm.isnumeric():
                    hh = int(hh)
                    mm = int(mm)
                    if hh <= 24 and mm <= 60:
                        #return(word)
                        return('{:0>2}'.format(hh) + ':' + '{:0>2}'.format(mm))

        elif 'pm' in word or 'am' in word: # for hh am, hh pm format (10 am, 9 pm)
            if len(word) == 2:
                hh = splitted_string[splitted_string.index(word) - 1]
                if len(hh) <= 2:
                    if hh.isnumeric():
                        if int(hh) <= 12:
                            return('{:0>2}'.format(hh) + word.lower())
            
            elif 2 < len(word) <= 4: # for hpm ham (1pm, 10am, etc.)
                word = word.lower()
                if 'pm' in word:
                    hh = word.split('pm')[0]
                    if hh.isnumeric():
                         if int(hh) <= 12:
                             return('{:0>2}'.format(hh) + 'pm')
                             
                elif 'am' in word:
                    hh = word.split('am')[0]
                    if hh.isnumeric():
                         if int(hh) <= 12:
                             return('{:0>2}'.format(hh) + 'am')

        elif word.isnumeric() and int(word) <= 23 and not ('pm' in splitted_string or 'am' in splitted_string):
                return('{:0>2}'.format(word) + ':00')
    
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
                local_time = arrow.get(datetime.now(), tz)
                
                if 'am' in time_string or 'pm' in time_string:
                    formatted_time = local_time.format('YYYY-MM-DD') + ' ' + time_string + local_time.format(' ZZ')
                    try:
                        my_time = arrow.get(formatted_time, 'YYYY-MM-DD hha ZZ')
                    except:
                        my_time = arrow.now(tz) #.format('hha')

                else:
                    formatted_time = local_time.format('YYYY-MM-DD') + ' ' + time_string + local_time.format(':ss ZZ')
                    try:
                        my_time = arrow.get(formatted_time, 'YYYY-MM-DD HH:mm:ss ZZ')
                    except:
                        my_time = arrow.now(tz) #.format('HH:mm')
                
                output_message = ''
                for zone in timezonelist:
                    zone_time = my_time.to(zone)
                    hhmm_time = zone_time.format('HH:mm')
                    your_tz = ''
                    if zone == tz:
                        your_tz = ' <- Your timezone'
                    output_message += hhmm_time + ' (' + zone + ')' + your_tz + '\n'
                
                outputs.append([channel, output_message]) # , 'TimeBot'

        except KeyError:
            print('KeyError Exception')
