# coding=utf-8

import sys
import logging
import datetime
from threading import Thread
import paho.mqtt.client as mqtt
import os

LOG = logging.getLogger("Subscribe")


def on_connect(client, userdata, flags, rc):
    LOG.info("Connected with result code " + str(rc))


def on_message(client, userdata, msg):
    epoch = datetime.datetime.utcfromtimestamp(0)
    LOG.info("current time "+epoch)
    LOG.info("message "+str(msg.payload))
    LOG.info("Timestamp {} , Subscribe on {}, QoS Level is {}, Message is {}".format(
        datetime.datetime.now(),
        msg.topic,
        msg.qos,
        str(msg.payload)
    ))
    RESULTS_FILE = os.getenv('RESULTS_FILE')
    LOG.info("RESULTS_FILE "+RESULTS_FILE)
    try:
      with open(RESULTS_FILE,'a+') as f:
         f.write("OnMessage: "  + msg.payload + "\n")
    except:
      LOG.info("exception writing to result file")
    


class Subscribe(Thread):
    def __init__(self, host, port, **kwargs):
        super(Subscribe, self).__init__()

        self.kwargs = kwargs
        self.topic = self.kwargs['topic'] if 'topic' in self.kwargs else None
        self.qos = self.kwargs['qos'] if 'qos' in self.kwargs else 0

        self.sub_client = mqtt.Client("Subscribe")
        self.sub_client.connect(host, port=int(port), keepalive=60)
        self.sub_client.on_connect = on_connect
        self.sub_client.on_message = on_message

        self.sub_client.subscribe(topic=self.topic, qos=int(self.qos))

    def run(self):
        self.sub_client.loop_forever()

    def run_on_thread(self):
        self.sub_client.loop_forever()


def main(args):
    try:
        LOG.info("Subscribe on {0} , QoS Level is {1}".format(args.topic, args.qos))
        subscriber = Subscribe(
            args.host,
            args.port,
            topic=args.topic,
            qos=args.qos,
        )
        subscriber.run_on_thread()
    except Exception as e:
        LOG.error("%s" % (e.__str__()))
        sys.exit()
