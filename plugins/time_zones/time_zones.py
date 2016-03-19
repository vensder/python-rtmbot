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
            #outputs.append([data['channel'], "```Time zones plugin try to parse \"{}\" in channel {} from user {}```".format(data['text'], data['channel'], data['user']) ])

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

                for zone in timezonelist:
                    zone_time = my_time.to(zone)
                    hhmm_time = zone_time.format('HH:mm')
                    your_tz = ''
                    if zone == tz:
                        your_tz = ' <- Your timezone'
                    outputs.append([data['channel'], hhmm_time + ' (' + zone + ')' + your_tz])


        except KeyError:
            print('KeyError Exception')


'''
    def input(self, data):
        if "type" in data:
            try:
                if data["type"] == "message":
                    if "team" in data and "user" in data:
                        team_id = data["team"]
                        user_id = data["user"]
                        if team_id not in profiles:
                            profiles[team_id] = dict()
                        if user_id not in profiles[team_id]:
                            json_res = json.dumps(self.slack_client.api_call("users.info", user=data["user"]), ensure_ascii=False)
                            if debug:
                                print(type(json_res)) # for debugging
                                print(json_res) # for debugging
                                print(' ^^^ Try to get json.dumps of user info ^^^ ') # for debugging
                            #str_res = json_res #.decode("utf-8", "strict")
                            res = json.loads(json_res)
                            profiles[team_id][user_id] = {
                                                    "name": res["user"]["name"], 
                                                    #"profile": res["user"]["profile"], 
                                                    "tz": res["user"]["tz"],
                                                    "is_bot": res["user"]["is_bot"],
                                                    "real_name": res["user"]["real_name"],
                                                    "tz_offset": res["user"]["tz_offset"],
                                                    "tz_label": res["user"]["tz_label"],
                                                    }
                        data.update(profiles[team_id][user_id])
                        print('profiles: ', profiles)
                        #data["name"] = profiles[team_id][user_id]["name"]
                        #data["tz"] = profiles[team_id][user_id]["tz"]
                        #data["profile"] = profiles[team_id][user_id]["profile"]
                #elif data["type"] == "presence_change":
                else:
                    if debug:
                        print(data) # print data to stdout about any other events 
            except:
                print("Parsing of message data didn't quite work as expected")
                print(traceback.print_exc())
            function_name = "process_" + data["type"]
            dbg("got {}".format(function_name))
            for plugin in self.bot_plugins:
                plugin.register_jobs()
                plugin.do(function_name, data)
'''

