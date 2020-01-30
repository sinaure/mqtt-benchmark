#!/bin/bash
value=$(<payload.json)
mqtt-bench publish --host 192.168.1.207 --port 1883 --topic "latency" --qos 0 --thread-num 10 --publish-num 1 --message $value