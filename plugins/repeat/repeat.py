#import time
#crontable = [] # what for?
outputs = []

def process_message(data):
    if data['channel'].startswith("C"):
        print(data)
        outputs.append([data['channel'], "from repeat1 \"{}\" in channel {}".format(data['text'], data['channel']) ])
#        outputs.append(type(data))

