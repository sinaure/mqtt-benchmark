# MQTT Benchmark Client for Python

### Install

python setup.py install

### Publish
```sh
mqtt-bench publish --host 192.168.99.100 --port 1883 --topic "test" --qos 0 --thread-num 10 --publish-num 50 --message "I'm test" --user hub-iot --password hub-iot
```

### Subscribe
```sh
$ mqtt-bench subscribe --host 192.168.99.100 --port 1883 --topic "test" --qos 2
```