# coding=utf-8

import sys
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
        self.qos = int(self.kwargs['qos']) if 'qos' in self.kwargs else 0
        self.publish_num = int(self.kwargs['publish_num']) if 'publish_num' in self.kwargs else 1
        self.message = None

        self.push_client = mqtt.Client(
            client_id="",
            clean_session=True,
            userdata=None,
        )
        self.push_client.connect(host, port, keepalive=60)

    def run(self):
        self.push_client.loop_start()
        self.message = "{time} : {message}".format(
            time=datetime.datetime.now(),
            message=self.message,
        )
        for i in range(0, self.publish_num):
            message = self.message + ", {0}".format(i + 1)
            self.push_client.publish(self.topic, message, qos=self.qos)
            LOG.debug(message)

        self.push_client.loop_stop()
        self.push_client.disconnect()


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
    try:
        publish_client = Publish(
            args.host,
            args.port,
            topic=args.topic,
            qos=int(args.qos),
            publish_num=int(args.publish_num),
        )
        publish_client.message = "Thread{0}, {1}".format(seq + 1, args.message)
        publish_client.start()
    except Exception as e:
        LOG.error("%s" % (e.__str__()))
        sys.exit()

