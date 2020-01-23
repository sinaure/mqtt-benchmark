# coding=utf-8

import sys
import logging
import datetime
import time
import json
import random
from threading import Thread
import paho.mqtt.client as mqtt

LOG = logging.getLogger("Publish")


class Publish(Thread):
    def __init__(self, host, port, **kwargs):
        super(Publish, self).__init__()
        LOG.info("init method")
        self.topic = kwargs['topic'] if 'topic' in kwargs else None
        self.qos = kwargs['qos'] if 'qos' in kwargs else 0
        self.publish_num = int(kwargs['publish_num']) if 'publish_num' in kwargs else 1
        self.username = kwargs['username'] if 'username' in kwargs else None
        self.password = kwargs['password'] if 'password' in kwargs else None

        self.push_client = mqtt.Client()
        self.push_client.on_publish = self.on_publish
        self.push_client.on_connect = self.on_connect
        
        
        if self.username!= None and self.password != None: 
            self.push_client.username_pw_set(self.username, self.password)

        LOG.info("connecting to "+ host+ ":"+ port)
        self.push_client.connect(host, port=int(port), keepalive=60)
        LOG.info("after connecting")

    def on_publish(client, userdata, mid):
        LOG.info("on publish callback")
    
    def on_connect(self, client, userdata, flags, rc):
        LOG.info("Connected with result code " + str(rc))
            
    def run(self):
        LOG.info("run method")
        self.push_client.loop_start()
        #self.message = "{time} : {message}".format(
        #    time=datetime.datetime.now(),
        #    message=self.message,
        #)
        for i in range(0, self.publish_num):
            modified_message = self.message
            self.push_client.publish(self.topic, self.message, qos=self.qos)
            

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
            password=args.password
        )
        LOG.info("message creating")
        publish_client.message = args.message
        LOG.info("client starting")
        publish_client.start()
    except Exception as e:
        LOG.error("%s" % (e.__str__()))
        sys.exit()

