# MQTT Benchmark Client for Python

### Install


* create binding on amq.topic with * key towards "test" queue
* Unistall and reinstall at every dev step

```
python setup.py install
pip uninstall mqtt-benchmark
```

### Generic Publish
```
mqtt-bench publish --host 192.168.99.100 --port 1883 --topic "test" --qos 0 --thread-num 10 --publish-num 50 --message "I'm test" --username hub-iot --password hub-iot
```
### Publish to mqtt bridge
```
mqtt-bench publish --host 192.168.99.100 --port 1883 --topic "diatomic/paris" --qos 0 --thread-num 10 --publish-num 50 --message '{"senml" : [{"bn":"urn:sosa:Sensor:00sfsf08","n":"incoming","u":"count","v":1200},{"n":"outgoing","u":"count","v":506}]}' --senml
```

### Subscribe
```
mqtt-bench subscribe --host 192.168.99.100 --port 1883 --topic "test" --qos 2 --file output.txt --interval 20
```

### Latency measurement publish
```
mqtt-bench publish --host 192.168.99.100 --port 1883 --topic "test" --qos 0 --thread-num 10 --publish-num 50 --message $(($(date +%s%N)/1000000))
```
