# MQTT Benchmark Client for Python

### Install


* create binding on amq.topic with * key towards "test" queue
* Unistall and reinstall at every dev step

```
python setup.py install
pip uninstall mqtt-benchmark
```

### Generic Publish
```sh
mqtt-bench publish --host 192.168.99.100 --port 1883 --topic "test" --qos 0 --thread-num 10 --publish-num 50 --message "I'm test" --username hub-iot --password hub-iot
```
### Publish to mqtt bridge
```sh
mqtt-bench publish --host 192.168.99.100 --port 1883 --topic "test" --qos 0 --thread-num 10 --publish-num 10 --amplitude 5000 --message '{"senml" : [{"bn":"urn:sosa:Sensor:00sfsf08","n":"incoming","u":"count","v":1200},{"n":"outgoing","u":"count","v":506}]}' --senml --sensors urn:sosa:Sensor:diatomicAA urn:sosa:Sensor:diatomicBB urn:sosa:Sensor:diatomicCC urn:sosa:Sensor:diatomicDD urn:sosa:Sensor:diatomicEE urn:sosa:Sensor:diatomicFF urn:sosa:Sensor:diatomicGG
```

### Subscribe
```sh
$ mqtt-bench subscribe --host 192.168.99.100 --port 1883 --topic "test" --qos 0
```