#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.dont_write_bytecode = True

import glob
import yaml
import json
import os
import sys
import time
import logging
from argparse import ArgumentParser
import traceback

from slackclient import SlackClient
from slackclient._channel import Channel
from websocket._exceptions import WebSocketConnectionClosedException


def dbg(debug_string):
    if debug:
        logging.info(debug_string)


class MySlackClient (SlackClient):
    pass


class MyChannel(Channel):
    
    def post_message(self, message, username, emoji):
        
        as_user = 'false'
        
        if username == '' and emoji == '':
            as_user = 'true'

        message_json = {
                    "channel": self.id, 
                    "text": message, 
                    "username": username, 
                    "as_user": as_user,
                    "icon_url": '',
                    "icon_emoji": emoji
                    }

        if debug:
            print('MESSAGE JSON:  ', message_json)
        
        self.server.api_call("chat.postMessage", **message_json)


class RtmBot(object):

    def __init__(self, token):
        self.last_ping = 0
        self.token = token
        self.bot_plugins = []
        self.slack_client = None

    def connect(self):
        """Convenience method that creates Server instance"""
        self.slack_client = MySlackClient(self.token)
        self.slack_client.rtm_connect()

    def reconnect(self):
        del self.slack_client
        self.slack_client = MySlackClient(self.token)
        self.slack_client.rtm_connect()

    def start(self):
        self.connect()
        self.load_plugins()
        while True:
            try:
                for reply in self.slack_client.rtm_read():
                    self.input(reply)
                self.crons()
                self.output()
                self.autoping()
                time.sleep(.1)
#            except Exception as e:
#                print(e)
            except (ConnectionResetError, TimeoutError, WebSocketConnectionClosedException):
                self.reconnect()

    def autoping(self):
        #hardcode the interval to 3 seconds
        now = int(time.time())
        if now > self.last_ping + 3:
            self.slack_client.server.ping()
            self.last_ping = now

    def input(self, data):
        if "type" in data:
            try:
                print("input: " + str(data))
                if data["type"] == "message":
                    #if "team" in data and "user" in data:
                    if "user" in data:
                        #team_id = data["team"]
                        #team_id = 'rtmbot'
                        user_id = data["user"]
                        #if team_id not in profiles:
                        #if 'rtmbot' not in profiles:
                            #profiles[team_id] = dict()
                            #profiles['rtmbot'] = dict()
                        if user_id not in profiles: #[team_id]:
                            json_res = json.dumps(self.slack_client.api_call("users.info", user=data["user"]), ensure_ascii=False)
                            
                            if debug:
                                print(data)
                                print(type(json_res))
                                print(json_res)
                                print(' ^^^ Try to get json.dumps of user info ^^^ ')
                            
                            res = json.loads(json_res)
                            #profiles[team_id][user_id] = {
                            profiles[user_id] = {
                                                    "name": res["user"]["name"], 
                                                    "tz": res["user"]["tz"],
                                                    "is_bot": res["user"]["is_bot"],
                                                    "real_name": res["user"]["real_name"],
                                                    "tz_offset": res["user"]["tz_offset"],
                                                    "tz_label": res["user"]["tz_label"],
                                                    }
                        #data.update(profiles[team_id][user_id])
                        data.update(profiles[user_id])
                        print('profiles: ', profiles)

                else:
                    if debug:
                        print(data) # print data to stdout about any other events 
            except:
                print("Parsing of message data didn't quite work as expected")
                print(traceback.print_exc())
            
            function_name = "process_" + data["type"]
            dbg("got {}".format(function_name))
            for plugin in self.bot_plugins:
                plugin.register_jobs()
                plugin.do(function_name, data)


    def output(self):
        for plugin in self.bot_plugins:
            limiter = False
            for output in plugin.do_output():
                channel = self.slack_client.server.channels.find(output[0])
                if channel is not None and output[1] is not None:
                    if limiter == True:
                        time.sleep(.1)
                        limiter = False
                    message = output[1]
                    if len(output) > 3:
                        username = output[2]
                        emoji = output[3]
                    else:
                        username = ''
                        emoji = ''
                    channel.__class__ = MyChannel
                    #channel.send_message("{}".format(message)) # send message to channel
                    channel.post_message("{}".format(message), username, emoji)
                    channel.__class__ = Channel
                    limiter = True

    def crons(self):
        for plugin in self.bot_plugins:
            plugin.do_jobs()

    def load_plugins(self):
        time.sleep(1)
        for plugin in glob.glob(directory+'/plugins/*'):
            sys.path.insert(0, plugin)
            sys.path.insert(0, directory+'/plugins/')
        for plugin in glob.glob(directory+'/plugins/*.py') + glob.glob(directory+'/plugins/*/*.py'):
            logging.info(plugin)
            name = plugin.split('/')[-1][:-3]
#            try:
            self.bot_plugins.append(Plugin(name))
#            except:
#                print "error loading plugin %s" % name


class Plugin(object):

    def __init__(self, name, plugin_config={}):
        self.name = name
        self.jobs = []
        self.module = __import__(name)
        self.register_jobs()
        self.outputs = []
        if name in config:
            logging.info("config found for: " + name)
            self.module.config = config[name]
        if 'setup' in dir(self.module):
            self.module.setup()

    def register_jobs(self):
        if 'crontable' in dir(self.module):
            for interval, function in self.module.crontable:
                self.jobs.append(Job(interval, eval("self.module."+function)))
            logging.info(self.module.crontable)
            self.module.crontable = []
        else:
            self.module.crontable = []

    def do(self, function_name, data):
        if function_name in dir(self.module):
            #this makes the plugin fail with stack trace in debug mode
            if not debug:
                try:
                    eval("self.module."+function_name)(data)
                except:
                    dbg("problem in module {} {}".format(function_name, data))
            else:
                eval("self.module."+function_name)(data)
        if "catch_all" in dir(self.module):
            try:
                self.module.catch_all(data)
            except:
                dbg("problem in catch all")

    def do_jobs(self):
        for job in self.jobs:
            job.check()

    def do_output(self):
        output = []
        while True:
            if 'outputs' in dir(self.module):
                if len(self.module.outputs) > 0:
                    logging.info("output from {}".format(self.module))
                    output.append(self.module.outputs.pop(0))
                else:
                    break
            else:
                self.module.outputs = []
        return output


class Job(object):

    def __init__(self, interval, function):
        self.function = function
        self.interval = interval
        self.lastrun = 0

    def __str__(self):
        return "{} {} {}".format(self.function, self.interval, self.lastrun)

    def __repr__(self):
        return self.__str__()

    def check(self):
        if self.lastrun + self.interval < time.time():
            if not debug:
                try:
                    self.function()
                except:
                    dbg("problem")
            else:
                self.function()
            self.lastrun = time.time()
            pass


class UnknownChannel(Exception):
    pass


def main_loop():
    if "LOGFILE" in config:
        logging.basicConfig(filename=config["LOGFILE"], level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info(directory)
    try:
        bot.start()
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        logging.exception('OOPS')


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '-c',
        '--config',
        help='Full path to config file.',
        metavar='path'
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    directory = os.path.dirname(sys.argv[0])
    if not directory.startswith('/'):
        directory = os.path.abspath("{}/{}".format(os.getcwd(),
                                directory
                                ))

    config = yaml.load(open(args.config or 'rtmbot.conf', 'r'))
    debug = config["DEBUG"]
    bot = RtmBot(config["SLACK_TOKEN"])
    site_plugins = []
    files_currently_downloading = []
    job_hash = {}
    profiles = {}

    if "DAEMON" in config:
        if config["DAEMON"]:
            import daemon
            with daemon.DaemonContext():
                main_loop()
    main_loop()

