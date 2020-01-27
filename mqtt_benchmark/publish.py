# coding=utf-8

import sys
import logging
import datetime
import time
import json
import random
from threading import Thread
import threading
from multiprocessing import Process, Value, Lock
import paho.mqtt.client as mqtt

logging.basicConfig(filename='logs.txt', filemode='w', level=logging.DEBUG)
LOG = logging.getLogger("Publish")

threads = list()


class Counter(object):
    def __init__(self, initval=0):
        self.val = Value('i', initval)
        self.lock = Lock()

    def increment(self):
        with self.lock:
            self.val.value += 1
            LOG.info("added thread : "+self.val.value)

    def value(self):
        with self.lock:
            return self.val.value

class Publish(Thread):
    def __init__(self, host, port,threadNumber,counter, **kwargs):
        Thread.__init__(self)
        LOG.info("init method")
        self.counter = counter
        self.topic = kwargs['topic'] if 'topic' in kwargs else None
        self.message = kwargs['message'] if 'message' in kwargs else None
        self.qos = kwargs['qos'] if 'qos' in kwargs else 0
        self.publish_num = int(kwargs['publish_num']) if 'publish_num' in kwargs else 1
        self.username = kwargs['username'] if 'username' in kwargs else None
        self.password = kwargs['password'] if 'password' in kwargs else None
        self.thread_num = kwargs['thread_num'] if 'thread_num' in kwargs else 1

        self.push_client = mqtt.Client("publisher"+str(threadNumber))
        self.publisherId = "publisher"+str(threadNumber)
        self.push_client.on_publish = self.on_publish
        self.push_client.on_connect = self.on_connect
        self.push_client.on_disconnect = self.on_disconnect
        
        if self.username!= None and self.password != None: 
            self.push_client.username_pw_set(self.username, self.password)

        LOG.info("connecting to "+ host+ ":"+ port)
        self.push_client.connect(host, port=int(port), keepalive=60)

    def on_publish(client, userdata, mid):
        LOG.info("on publish callback")
    
    def on_connect(self, client, userdata, flags, rc):
        LOG.info("Connected with result code " + str(rc))
        self.counter.increment()
    
    def on_disconnect(client, userdata, rc):
        LOG.info("disconnecting reason  "  +str(rc))
            
    def run(self):
        
        start_time = int((time.time() * 1000))
        LOG.info("START run method for : {1} at {0}".format(
            start_time,
            self.publisherId
            ))
        
        self.push_client.loop_start()
        
        
        while self.counter.value() < int(self.thread_num):
            time.sleep(0.1)
        
        self.publish()
        self.push_client.loop_stop()
        self.push_client.disconnect()
        end_time = int((time.time() * 1000))
        
        LOG.info("END run method for : {1} at {0}".format(
            end_time,
            self.publisherId
            ))
        
        LOG.info("it tooks {0} ms to complete run for {1}".format(
            end_time - start_time,
            self.publisherId
            )) 
        
    def publish(self):
        start_time = int((time.time() * 1000))
        LOG.info("START publish method for client : {1} at : {0}".format(
            start_time,
            self.publisherId
            ))
        for i in range(0, self.publish_num):
            obj = json.loads(self.message)
            obj["time"] = int((time.time() * 1000))
            obj["publisherId"] = self.publisherId
            self.push_client.publish(self.topic, json.dumps(obj), qos=self.qos)    
        
        end_time = int((time.time() * 1000))
        LOG.info("END publish method for clients : {1} at : {0} ".format(
            end_time,
            self.publisherId
            ))   
        LOG.info("it tooks {0} ms to complete publish for {1}".format(
            end_time - start_time,
            self.publisherId
            )) 
            
def main(args):
    counter = Counter(0)
    start_time = int((time.time() * 1000))
    LOG.info("{0} - START Main method - connected clients : {1}".format(
            start_time,
            str(counter.value())
            ))
    thread_num = int(args.thread_num) if args.thread_num is not None else 1
    if thread_num > 0:
        for seq in range(0, thread_num):
            thread_start(args, seq + 1, counter)
    
    
    for t in threads:
        t.join()
    
    LOG.info("End join")
    
    end_time = int((time.time() * 1000))
    
    LOG.info("{0} - END Main method connected clients : {1}".format(
            end_time,
            str(counter.value())
            ))
        
    
    LOG.info("It took {0} ms to execute the test".format(
            end_time - start_time
            ))       
    #for index, thread in enumerate(threads):
    #    LOG.info("Main    : before joining thread %d. at : "+str((time.time() * 1000)), index)
    #    thread.join()
    #    LOG.info("Main    : thread %d done at : "+str((time.time() * 1000)), index)        

def thread_start(args, seq, counter):
    LOG.info("thread_start method "+seq+1)
    try:
        publish_client = Publish(
            args.host,
            args.port,
            seq,
            counter,
            topic=args.topic,
            qos=int(args.qos),
            publish_num=int(args.publish_num),
            username=args.username,
            password=args.password,
            message=args.message,
            thread_num=args.thread_num
        )
        threads.append(publish_client)
        publish_client.start()
        
        
    except Exception as e:
        LOG.error("%s" % (e.__str__()))
        sys.exit()

