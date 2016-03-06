# -*- coding: utf-8 -*-
#import time
#crontable = [] # what for?
outputs = []

def process_message(data):
    #if data['channel'] == 'general':
    #if data['channel'] == 'C0DEMSUG5':
    print('type(data): ', type(data))
    print('data: ', data)
    outputs.append([data['channel'], "Hello from 'repeat' plugin \"{}\" in channel {} from user {}".format(data['text'], data['channel'], data['user']) ])
    
    if '@time' in data['text']:
        print('time?')
        outputs.append([data['channel'], " time?" + 'user: ' + data['real_name']])
    
