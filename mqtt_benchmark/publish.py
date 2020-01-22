# coding=utf-8

import sys
import logging
import datetime
import time
import json
import random
from threading import Thread
import paho.mqtt.client as mqtt
import datetime

LOG = logging.getLogger("Publish")
import math

class Publish(Thread):
    def __init__(self, host, port, **kwargs):
        super(Publish, self).__init__()
        LOG.info("init method")
        LOG.info(kwargs)
        self.topic = kwargs['topic'] if 'topic' in kwargs else None
        self.qos = kwargs['qos'] if 'qos' in kwargs else 0
        self.publish_num = int(kwargs['publish_num']) if 'publish_num' in kwargs else 1
        self.username = kwargs['username'] if 'username' in kwargs else None
        self.password = kwargs['password'] if 'password' in kwargs else None
        self.senml = kwargs['senml'] if 'senml' in kwargs else False
        self.sensors = kwargs['sensors'] if 'sensors' in kwargs else None
        
        self.amplitude = kwargs['amplitude'] if 'amplitude' in kwargs else 10000 # max 10000
        self.delta = kwargs['delta'] if 'delta' in kwargs else 360 # data production starts in 360 min from midnight
        self.period = kwargs['period'] if 'period' in kwargs else 720 # repeats every 12h
        
        self.push_client = mqtt.Client()

        
        if self.username!= None and self.password != None: 
            self.push_client.username_pw_set(self.username, self.password)

        LOG.info("connecting to "+ host+ ":"+ port)
        self.push_client.connect(host, port=int(port), keepalive=60)
        LOG.info("after connecting")

    def oscillatoryFunc(self):
        now = datetime.datetime.now()
        minutes = now.hour*60 + now.minute
        if minutes < 360 or minutes > 1080:
            return 0
        else:
            return (self.amplitude*math.sin(math.pi*(minutes-self.delta)/self.period) + self.amplitude)  
        
    def run(self):
        LOG.info("run method")
        self.push_client.loop_start()
        #self.message = "{time} : {message}".format(
        #    time=datetime.datetime.now(),
        #    message=self.message,
        #)
        for i in range(0, self.publish_num):
            
            #modified_message = self.message + ", {0}".format(i + 1)
            modified_message = self.message
            
            if self.senml == True :
                
                message_as_json = json.loads(self.message)
                    
                for x in message_as_json["senml"]:
                    x["v"]=oscillatoryFunc()
                    LOG.debug(x)
                
                modified_message = json.dumps(message_as_json["senml"])    
                LOG.debug("Publishing")
                LOG.debug(modified_message)
                
            
            self.push_client.publish(self.topic, modified_message, qos=self.qos)
            

        self.push_client.loop_stop()
        self.push_client.disconnect()


def main(args):
    LOG.info("main method")
    LOG.info(args)
    thread_num = int(args.thread_num) if args.thread_num is not None else 1
    if thread_num > 0:
        for seq in range(0, thread_num):
            push(args, seq)
    else:
        count = 0
        while 1:
            push(args, count)
            count += 1
            time.sleep(1)


def push(args, seq):
    LOG.info("push method")
    try:
        publish_client = Publish(
            args.host,
            args.port,
            topic=args.topic,
            qos=int(args.qos),
            publish_num=int(args.publish_num),
            username=args.username,
            password=args.password,
            senml=args.senml
        )
        LOG.info("message creating")
        publish_client.message = args.message
        LOG.info("client starting")
        publish_client.start()
    except Exception as e:
        LOG.error("%s" % (e.__str__()))
        sys.exit()

