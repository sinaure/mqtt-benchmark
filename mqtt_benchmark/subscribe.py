# coding=utf-8

import logging
from threading import Thread
import paho.mqtt.client as mqtt

LOG = logging.getLogger("Subscribe")


def on_connect(client, userdata, flags, rc):
    LOG.Info("Connected with result code " + str(rc))


def on_message(client, userdata, msg):
    LOG.debug("[{0}] - {1}".format(msg.topic, str(msg.payload)))


class Subscribe(Thread):
    def __init__(self, host, port, **kwargs):
        super(Subscribe, self).__init__()

        self.kwargs = kwargs
        self.topic = self.kwargs['topic'] if 'topic' in self.kwargs else None
        self.qos = self.kwargs['qos'] if 'qos' in self.kwargs else 0

        self.sub_client = mqtt.Client("Subscribe")
        self.sub_client.connect(host, port, 60)
        self.sub_client.on_connect = on_connect
        self.sub_client.on_message = on_message
        self.sub_client.subscribe(topic=self.topic, qos=int(self.qos))

    def run(self):
        self.sub_client.loop_forever()

    def run_on_thread(self):
        self.sub_client.loop_forever()


def main(args):
    LOG.info("Subscribe on {0} , QoS Level is {1}".format(args.topic, args.qos))
    subscriber = Subscribe(
        args.host,
        args.port,
        topic=args.topic,
        qos=args.qos,
    )
    subscriber.run_on_thread()
