#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from configparser import ConfigParser
from yandex_translate import YandexTranslate
from os import path

outputs = []

parser = ConfigParser()
parser.read(path.dirname(path.realpath(__file__)) + '/translator.conf')

token = parser.get('yandex', 'token')


def process_message(data):
    if 'text' in data:
        try:
            text = data['text']
            channel = data['channel']
            detected_lang = 'en' #default lang

            if '@translate' in text:
                translate = YandexTranslate(token)
                phrase_to_translate = text.replace('@translate', '').strip()
                print('phrase_to_translate: ', phrase_to_translate)

                if phrase_to_translate != '':

                    try:
                        detected_lang = translate.detect(phrase_to_translate)
                        print('detected_lang: ', detected_lang)

                    except Exception as e:
                        outputs.append([channel, str(e) + ". Can't detect the language", 'Translator', ':exclamation:'])
                        print('Exception in ipcalculator: ', e)
                        print('detected_lang: ', detected_lang)


                    if detected_lang != 'ru':
                        direction = detected_lang + '-ru'
                        if detected_lang == 'en':
                            flag_from = ':flag-us:'
                        else:
                            flag_from = ':flag-' + detected_lang + ':'

                        try:
                            translate_dict = translate.translate(phrase_to_translate, direction)
                            if translate_dict['code'] == 200:
                                translation = translate_dict['text'][0]
                                outputs.append([channel, flag_from + ':flag-ru:' + ' ' + translation, 'Translator', ':flag-ru:'])
                            else:
                                outputs.append([channel, 'Code: ' + translate_dict['code']])
                        except:
                            outputs.append([channel, 'Something go wrong'])

                    if detected_lang == 'ru':

                        try:
                            translate_dict = translate.translate(phrase_to_translate, 'ru-en')
                            if translate_dict['code'] == 200:
                                translation = translate_dict['text'][0]
                                outputs.append([channel, translation, 'Translator', ':flag-us:', ])
                            else:
                                outputs.append([channel, 'Code: ' + translate_dict['code']])
                        except:
                            outputs.append([channel, 'Something go wrong'])

                else:
                    outputs.append([channel, 'Write anything, please', 'Translator', ':flag-us:'])


        except KeyError:
            print('KeyError Exception')
