#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#import time
#crontable = [] # what for?
import arrow
from datetime import datetime
#from pytz import timezone
outputs = []

# set default Time Zone
tz = 'US/Eastern'


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
    #if data['channel'] == 'general':
    #if data['channel'] == 'C0DEMSUG5':
    print('type(data): ', type(data))
    print('data: ', data)
    
    if 'text' in data:
        try:
            text = data['text']
                    
            channel = data['channel']
            #outputs.append([data['channel'], "```Time zones plugin try to parse \"{}\" in channel {} from user {}```".format(data['text'], data['channel'], data['user']) ])

            if '@time' in text:
                if 'tz' in data:
                    tz = data['tz']
                else:
                    tz = 'UTC'
                timezone_set = {'America/New_York', 'Europe/Minsk'}
                timezone_user = {tz}
                timezonelist = list(timezone_set | timezone_user)
                timezonelist.sort
                time_string = time_parsing(text, tz)
                print(time_string)
                
                local_time = arrow.get(datetime.now(), tz)
                string_time = local_time.format('YYYY-MM-DD') + ' ' + time_string + local_time.format(':ss ZZ')
                my_time = arrow.get(string_time, 'YYYY-MM-DD HH:mm:ss ZZ')
                print(type(my_time))

                for zone in timezonelist:
                    zone_time = my_time.to(zone)
                    hhmm_time = zone_time.format('HH:mm')
                    your_tz = ''
                    if zone == tz:
                        your_tz = ' <- Your timezone'
                    outputs.append([data['channel'], hhmm_time + ' (' + zone + ')' + your_tz])

                #outputs.append([channel, str(local.humanize())])
                print('echo: ', text)
                #outputs.append([data['channel'], " time?" + 'user: ' + data['real_name']])

        except KeyError:
            print('KeyError Exception')

        

