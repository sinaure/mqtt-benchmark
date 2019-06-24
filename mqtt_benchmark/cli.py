# coding=utf-8

import sys
import argparse
import logging
import textwrap

from mqtt_benchmark import publish
from mqtt_benchmark import subscribe
from mqtt_benchmark.common import logs

LOG = logging.getLogger("CLI")

__header__ = textwrap.dedent("""
  _  _  _   _  _____  ___   _
 | \| || | | ||_   _|/ __| (_)    _ __      __ _     __
 | .` || |_| |  | | | (__  | | _ | '  \  _ / _` | _ / _|
 |_|\_| \___/   |_|  \___| |_|(_)|_|_|_|(_)\__,_|(_)\__|

""")


def get_parser():
    parser = argparse.ArgumentParser(
        prog='mqtt-bench',
        formatter_class=argparse.RawTextHelpFormatter,
        description='MQTT Benchmark Client for python\n\n%s' % __header__,
    )

    options_parser = argparse.ArgumentParser(add_help=False)

    options_parser.add_argument("--host", help="MQTT broker host address", default="localhost")
    options_parser.add_argument("--port", help="MQTT broker bind port", default=1883)
    options_parser.add_argument("--topic", help="MQTT broker topic name")
    options_parser.add_argument("--qos", help="MQTT broker qos level", default=0)
    options_parser.add_argument("--username", help="MQTT broker username")
    options_parser.add_argument("--password", help="MQTT broker password")
    
    subparsers = parser.add_subparsers(help='types of mqtt parser')
    
    p_parser = subparsers.add_parser("publish", parents=[options_parser])
    s_parser = subparsers.add_parser("subscribe", parents=[options_parser])
    
    p_parser.add_argument("--message", help="Publish a message", default="I'm a test")
    p_parser.add_argument("--thread-num", help="Publish thread number", default=1)
    p_parser.add_argument("--publish-num", help="Publish message seq number", default=1)

    return parser


def main():

    sh = logging.StreamHandler()
    sh.setFormatter(logs.color_format())
    sh.setLevel(logging.WARNING)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(sh)
    sh.setLevel(logging.DEBUG)

    parser = get_parser()
    args = parser.parse_args()

    LOG.info(sys.argv) 
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit()
        
    if sys.argv[1] != "publish" and   sys.argv[0] != "subscribe":  
        LOG.error('First positional argument not accepted (chose between subscribe or publish)')
        sys.exit()
    
    if sys.argv[1] == 'publish':
        if args.message is not None:
            publish.main(args)
        else:
            parser.print_help()

    elif sys.argv[1] == 'subscribe':
        if args.topic is not None:
            subscribe.main(args)
        else:
            parser.print_help()


if __name__ == '__main__':
    main()
