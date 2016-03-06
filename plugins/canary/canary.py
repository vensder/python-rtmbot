#import time
from time import gmtime, strftime
outputs = []

def canary():
    #NOTE: you must add a real channel ID for this to work
    localtime = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    outputs.append(["general", "bot started: " + str(localtime)])

canary()
