#import time
from time import gmtime, strftime
outputs = []

def canary():
    #NOTE: you must add a real channel ID for this to work
#    localtime = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    localtime = strftime("%a, %d %b %Y %H:%M", gmtime())
    outputs.append(["bots", "bot started at @time: " + str(localtime)])

canary()