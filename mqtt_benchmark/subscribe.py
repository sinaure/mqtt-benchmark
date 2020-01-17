# coding=utf-8

import sys
import logging
import datetime
from threading import Thread
import paho.mqtt.client as mqtt
import time
LOG = logging.getLogger("Subscribe")

def on_connect(client, userdata, flags, rc):
    LOG.info("Connected with result code " + str(rc))
    

def on_subscribe(mqttc, obj, mid, granted_qos):
    LOG.info("Subscribed: " + str(mid) + " " + str(granted_qos))        

def on_message(client, userdata, msg):
    LOG.debug("{0} : Subscribe on {1}, QoS Level is {2}, Message is {3}".format(
        datetime.datetime.now(),
        msg.topic,
        msg.qos,
        str(msg.payload.decode("utf-8"))
        ))
    productionTime= msg.payload.decode("utf-8")
    LOG.debug("productionTime: {0}".format(productionTime))
    if productionTime.isnumeric():
        LOG.info("Latency: {0}".format(int((time.time() * 1000)) - int(productionTime)))
 
class Subscribe(Thread):
    def __init__(self, host, port, **kwargs):
        super(Subscribe, self).__init__()
        
        self.kwargs = kwargs
        self.topic = self.kwargs['topic'] if 'topic' in self.kwargs else None
        self.qos = self.kwargs['qos'] if 'qos' in self.kwargs else 0

        self.sub_client = mqtt.Client("EGM-subscriber")
        self.sub_client.on_connect = on_connect
        self.sub_client.on_message = on_message
        self.sub_client.on_subscribe = on_subscribe
        self.sub_client.connect(host, port, keepalive=60)
        
        
        time.sleep(2)
            
        LOG.info("subscribing...")    
        self.sub_client.subscribe(topic=self.topic, qos=int(self.qos))
    
        
    def run(self):
        self.sub_client.loop_forever()



def main(args):
    try:
        LOG.info("Main method topic: {0} , QoS Level is {1}".format(args.topic, args.qos))
        subscriber = Subscribe(
            args.host,
            int(args.port),
            topic=args.topic,
            qos=args.qos,
        )
        subscriber.run()
    except Exception as e:
        LOG.error("%s" % (e.__str__()))
        sys.exit()
