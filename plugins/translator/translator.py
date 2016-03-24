#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from configparser import ConfigParser
from yandex_translate import YandexTranslate
from os import path

parser = ConfigParser()
parser.read(path.dirname(path.realpath(__file__)) + '/translator.conf')

token = parser.get('yandex', 'token')

def process_message(data):
    
    if 'text' in data:
        try:
            text = data['text']
            channel = data['channel']

            if 'translate it' in text or 'Translate it' in text:
                translate = YandexTranslate(token)
                phrase_to_translate = text.lstrip('Ttranslte i').lstrip(': ')
                
                try:
                    translate_dict = translate.translate(phrase_to_translate, 'en-ru')
                    if translate_dict['code'] == 200:
                        translate = translate_dict['text'][0]
                        outputs.append([data['channel'], translate ])
                    else:
                        outputs.append([data['channel'], 'Code: ' + translate_dict['code'] ])
                except:
                    outputs.append([data['channel'], 'Something go wrong' ])

        except KeyError:
            print('KeyError Exception')
