#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ipcalc

outputs = []

def process_message(data):
    
    if 'text' in data:
        try:
            text = data['text']
            channel = data['channel']

            if 'ipcalc' in text:
                output_string = ''
                network = ipcalc.Network('10.0.0.100/24')
                network_string = text.lstrip('ipcalc ') #text.lstrip('ipcalc ').strip('abcdefghijklmnopqrstuvwxyz ')
                
                try:
                    network = ipcalc.Network(network_string)
                except:
                    outputs.append([data['channel'], 'Try something like: ```ipcalc 10.0.0.100/24``` or ```ipcalc 172.16.0.0/16```' ])
                
                try:
                    output_string += '```'
                    output_string += str(network.network()) + '/' + str(network.mask) + ' (network/mask)\n'
                    output_string += str(network.host_first()) + ' (first host)\n' # IP('172.16.42.1')
                    output_string += str(network.host_last()) + ' (last host)\n' # IP('172.16.42.2')
                    output_string += str(network.netmask()) + ' (netmask)\n' # 30
                    output_string += str(network.size()) + ' (size)\n'  # 4
                    output_string += str(network.info()) + ' (network type)\n' # 'PRIVATE'
                    output_string += '```'

                    outputs.append([data['channel'], output_string ])

                except:
                    outputs.append([data['channel'], 'Try something like 10.0.0.100/24 or 172.16.0.0/16' ])


        except KeyError:
            print('KeyError Exception')
