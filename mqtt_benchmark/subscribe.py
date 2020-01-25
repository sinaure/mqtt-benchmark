# coding=utf-8

import sys
import logging
import datetime
from threading import Thread
import paho.mqtt.client as mqtt
import time
import os
LOG = logging.getLogger("Subscribe")



        

 
class Subscribe(Thread):
    def __init__(self, host, port, **kwargs):
        super(Subscribe, self).__init__()
        
        self.kwargs = kwargs
        self.topic = self.kwargs['topic'] if 'topic' in self.kwargs else None
        self.qos = self.kwargs['qos'] if 'qos' in self.kwargs else 0
        self.output_file = self.kwargs['file'] if 'file' in self.kwargs else None
        self.interval = self.kwargs['interval'] if 'interval' in self.kwargs else None

        self.sub_client = mqtt.Client("EGM-subscriber")
        self.sub_client.on_connect = self.on_connect
        self.sub_client.on_message = self.on_message
        self.sub_client.on_subscribe = self.on_subscribe
        self.sub_client.connect(host, port, keepalive=60)
        
        time.sleep(2)
            
        LOG.info("subscribing...")    
        self.sub_client.subscribe(topic=self.topic, qos=int(self.qos))
    
        
    def run(self):
        if self.interval is None:
            self.sub_client.loop_forever()
        else:
            self.sub_client.loop_start()
            LOG.info("Disconnecting after {0} seconds".format(self.interval))
            time.sleep(int(self.interval)) 
            self.sub_client.disconnect() 
            self.sub_client.loop_stop()

    def on_message(self, client, userdata, msg):
        LOG.debug("{0} : Subscribe on {1}, QoS Level is {2}, Message is {3}".format(
            datetime.datetime.now(),
            msg.topic,
            msg.qos,
            str(msg.payload.decode("utf-8"))
            ))
        productionTime= msg.payload.decode("utf-8")
        if productionTime.isnumeric():
            latency = int((time.time() * 1000)) - int(productionTime)
            LOG.info("Latency: {0}".format(latency))
            if os.path.exists(self.output_file):
                append_write = 'a' # append if already exists
            else:
                append_write = 'w' # make a new file if not
            with open(self.output_file, append_write) as myfile:
                myfile.write(str(productionTime)+";"+str(latency)+"\n")
    
           

    def on_subscribe(self, client, obj, mid, granted_qos):
        LOG.info("Subscribed: " + str(mid) + " " + str(granted_qos))
        LOG.info("output to : {0}".format(self.output_file))
    
    def on_connect(self, client, userdata, flags, rc):
        LOG.info("Connected with result code " + str(rc))
    
        
def main(args):
    try:
        LOG.info("Main method topic: {0} , QoS Level is {1}".format(args.topic, args.qos))
        subscriber = Subscribe(
            args.host,
            int(args.port),
            topic=args.topic,
            qos=args.qos,
            file=args.file,
            interval=args.interval
        )
        subscriber.run()
    except Exception as e:
        LOG.error("%s" % (e.__str__()))
        sys.exit()
