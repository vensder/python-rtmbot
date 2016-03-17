import http.client
from configparser import ConfigParser
from urllib.parse import urlencode

import os

print('getcwd: ', os.getcwd())
print('pathdirname: ', os.path.dirname(os.path.realpath(__file__)))

parser = ConfigParser()
parser.read(os.path.dirname(os.path.realpath(__file__)) + '/telegram.conf')

token = parser.get('bot', 'token')
telegram_chat = parser.get('user', 'telegram-id')
slack_user = parser.get('user', 'slack-id')
slack_name = parser.get('user', 'slack-name')


def send_to_telegram(text):
    
    global token, telegram_chat
    
    conn = http.client.HTTPSConnection("api.telegram.org")
    conn.request('GET', '/' + token + '/sendMessage?' + urlencode({'text': text}) + '&chat_id=' + telegram_chat)

    r1 = conn.getresponse()
    print('telegram response: ', r1.status, r1.reason)


def process_message(data):

    global slack_user, slack_name
    
    if 'text' in data:
        try:
            text = data['text']
#            channel = data['channel']
#            user = data['user'] #TODO add 'sent from <user>'
            
            if slack_user in text:
                send_to_telegram(text.replace(slack_user, 'vensder'))

        except KeyError:
            print('KeyError Exception')
