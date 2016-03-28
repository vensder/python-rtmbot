#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ipcalc

outputs = []

def process_message(data):
    
    if 'text' in data:
        try:
            text = data['text']
            channel = data['channel']
            except_phrase = 'Try something like this: ```@ipcalc 10.0.0.0/24```'

            if '@ipcalc' in text and except_phrase not in text:
                
                output_string = ''
                emoji = ':spider_web:'
                except_emoji = ':exclamation:'
                bot_name = 'ip calculator'
                
                network = ipcalc.Network('10.0.0.0/24')
                network_string = text.strip(' @ipcalc ') #text.lstrip('ipcalc ').strip('abcdefghijklmnopqrstuvwxyz ')
                
                try:
                    network = ipcalc.Network(network_string)
                except Exception as e:
                    outputs.append([data['channel'], str(e) + '. ' + except_phrase, bot_name, except_emoji ])
                    print('Exception in ipcalculator: ', e)
                    print('network: ', network_string)
                
                try:
                    output_string += '```'
                    output_string += str(network.network()) + '/' + str(network.mask) + ' (network/mask)\n'
                    output_string += str(network.host_first()) + ' (first host)\n' # IP('172.16.42.1')
                    output_string += str(network.host_last()) + ' (last host)\n' # IP('172.16.42.2')
                    output_string += str(network.netmask()) + ' (netmask)\n' # 30
                    output_string += str(network.size()) + ' (size)\n'  # 4
                    output_string += str(network.info()) + ' (network type)\n' # 'PRIVATE'
                    output_string += '```'

                    outputs.append([data['channel'], output_string, bot_name, emoji ])

                except Exception as e:
                    outputs.append([data['channel'], str(e) + '. ' + except_phrase, bot_name, except_emoji ])
                    print('Exception in ipcalculator: ',e)
                    print('network: ', network_string)


        except KeyError as e:
            print('KeyError Exception in ipcalculator.py: ', e)
            print(data)
