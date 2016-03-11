# -*- coding: utf-8 -*-

outputs = []

def process_message(data):
    print("\nBEGIN PROCESS MESSAGE\n")
    print('\ntype(data):\n ', type(data))
    print('\ndata: \n', data)
    #text = data['text']
    #channel = data['channel']
    #outputs.append([data['channel'], "Hello from 'repeat' plugin \"{}\" in channel {} from user {}".format(data['text'], data['channel'], data['user']) ])
    print('\nEND PROCESS MESSAGE\n')


'''
#./rtmbot.py

#BEGIN PROCESS MESSAGE
data:  {'text': 'bot started at @time: Fri, 11 Mar 2016 12:24', 
        'reply_to': None, 
        'type': 'message', 
        'user': 'U0QLT7CDS', 
        'channel': 'C0QN2S8J3', 
        'ts': '1457699039.000023'}

# END PROCESS MESSAGE


#BEGIN PROCESS MESSAGE
data: 
 {'reply_to': None, 
 'type': 'message', 
 'channel': 'C0QN2S8J3', 
 'user': 'U0QLT7CDS', 
 'text': 'bot started at @time: Fri, 11 Mar 2016 12:24', 
 'ts': '1457699093.000024'}
END PROCESS MESSAGE

{"user": {
        "is_admin": false, 
        "is_owner": false, 
        "team_id": "T0DET484Q", 
        "real_name": "Dmitry", 
        "color": "4bbe2e", 
        "deleted": false, 
        "tz_offset": 10800, 
        "profile": {
                    "image_72": "https://secure.gravatar.com/avatar/cc3d6d02dee2b5b5c81460cab4d9da14.jpg?s=72&d=https%3A%2F%2Fslack.global.ssl.fastly.net%2F66f9%2Fimg%2Favatars%2Fava_0016-72.png", 
                    "image_24": "https://secure.gravatar.com/avatar/cc3d6d02dee2b5b5c81460cab4d9da14.jpg?s=24&d=https%3A%2F%2Fslack.global.ssl.fastly.net%2F66f9%2Fimg%2Favatars%2Fava_0016-24.png",
                    "first_name": "Dmitry", 
                    "email": "vensder@gmail.com", 
                    "image_512": "https://secure.gravatar.com/avatar/cc3d6d02dee2b5b5c81460cab4d9da14.jpg?s=512&d=https%3A%2F%2Fslack.global.ssl.fastly.net%2F7fa9%2Fimg%2Favatars%2Fava_0016-512.png", 
                    "real_name": "Dmitry", 
                    "image_32": "https://secure.gravatar.com/avatar/cc3d6d02dee2b5b5c81460cab4d9da14.jpg?s=32&d=https%3A%2F%2Fslack.global.ssl.fastly.net%2F66f9%2Fimg%2Favatars%2Fava_0016-32.png", 
                    "image_192": "https://secure.gravatar.com/avatar/cc3d6d02dee2b5b5c81460cab4d9da14.jpg?s=192&d=https%3A%2F%2Fslack.global.ssl.fastly.net%2F7fa9%2Fimg%2Favatars%2Fava_0016-192.png", 
                    "real_name_normalized": "Dmitry", 
                    "image_48": "https://secure.gravatar.com/avatar/cc3d6d02dee2b5b5c81460cab4d9da14.jpg?s=48&d=https%3A%2F%2Fslack.global.ssl.fastly.net%2F66f9%2Fimg%2Favatars%2Fava_0016-48.png"
                        }, 
        "is_restricted": false, 
        "status": null, 
        "name": "vensder", 
        "is_ultra_restricted": false, 
        "tz_label": "Moscow Time", 
        "tz": "Europe/Moscow", 
        "is_primary_owner": false, 
        "is_bot": false, 
        "id": "U0DEX55DL"}, 
"ok": true}

 #^^^ Try to get json.dumps of user info ^^^ 

#BEGIN PROCESS MESSAGE
data: 
 {
 'type': 'message', 
 'tz': 'Europe/Moscow', 
 'user': 'U0DEX55DL', 
 'real_name': 'Dmitry', 
 'tz_offset': 10800, 
 'ts': '1457699161.000021', 
 'name': 'vensder', 
 'tz_label': 'Moscow Time', 
 'channel': 'C0DEMSUG5', 
 'text': 'первый текст', 
 'team': 'T0DET484Q', 
 'is_bot': False}
#END PROCESS MESSAGE


#BEGIN PROCESS MESSAGE
data: 
 {
 'type': 'message', 
 'tz': 'Europe/Moscow', 
 'user': 'U0DEX55DL', 
 'real_name': 'Dmitry', 
 'tz_offset': 10800, 
 'ts': '1457699183.000022', 
 'name': 'vensder', 
 'tz_label': 'Moscow Time', 
 'channel': 'C0DEMSUG5', 
 'text': 'второй текст', 
 'team': 'T0DET484Q', 
 'is_bot': False}
#END PROCESS MESSAGE


#BEGIN PROCESS MESSAGE
data: 
 {
 'type': 'message', 
 'previous_message': {
                    'type': 'message', 
                    'text': 'второй текст', 
                    'ts': '1457699183.000022', 
                    'user': 'U0DEX55DL'
                        }, 
 'subtype': 'message_changed', 
 'channel': 'C0DEMSUG5', 
 'hidden': True, 
 'message': {
            'type': 'message', 
            'text': 'второй текст редактированный', 
            'edited': {
                        'ts': '1457699205.000000', 
                        'user': 'U0DEX55DL'
                            }, 
            'user': 'U0DEX55DL', 
            'ts': '1457699183.000022'
                }, 
 'ts': '1457699205.000023', 
 'event_ts': '1457699205.157060'
     }

#END PROCESS MESSAGE

'''
