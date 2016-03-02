# coding=utf-8

import logging
import datetime
import time
from threading import Thread
import paho.mqtt.client as mqtt

LOG = logging.getLogger("Publish")


class Publish(Thread):

    def __init__(self, host, port, **kwargs):
        super(Publish, self).__init__()

        self.kwargs = kwargs
        self.topic = self.kwargs['topic'] if 'topic' in self.kwargs else None
        self.qos = self.kwargs['qos'] if 'qos' in self.kwargs else 0
        self.message = None

        self.push_client = mqtt.Client("Publish")
        self.push_client.connect(host, port)

    def run(self):
        self.message = "{time} : {message}".format(
            time=datetime.datetime.now(),
            message=self.message,
        )
        LOG.debug(self.message)
        self.push_client.publish(self.topic, self.message, qos=int(self.qos))


def main(args):

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
    publish_client = Publish(args.host, args.port, topic=args.topic, qos=args.qos,)
    publish_client.message = "{0}, {1}".format(args.message, seq + 1)
    publish_client.start()
