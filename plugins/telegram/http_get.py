import http.client
from configparser import ConfigParser

import os

print('getcwd: ', os.getcwd())
print('pathdirname: ', os.path.dirname(os.path.realpath(__file__)))

parser = ConfigParser()
parser.read(os.path.dirname(os.path.realpath(__file__)) + '/telegram.conf')
token = parser.get('bot', 'token')

conn = http.client.HTTPSConnection("api.telegram.org")

conn.request("GET", "/" + token + "/sendMessage?text=Python bot has just been started&chat_id=32200471")

r1 = conn.getresponse()
print(r1.status, r1.reason)

