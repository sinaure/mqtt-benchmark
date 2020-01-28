# MQTT Benchmark Client for Python

### Install


* create binding on amq.topic with * key towards "test" queue
* Unistall and reinstall at every dev step

```
pip uninstall mqtt-benchmark
python setup.py install
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
mqtt-bench subscribe --host 192.168.99.100 --port 1883 --topic "test" --qos 0 --file output.txt --interval 2000
```


### Latency measurement publish Datahub (payload == 100B)
```
mqtt-bench publish --host 192.168.1.207 --port 1883 --topic "latency" --qos 0 --thread-num 10 --publish-num 1 --message '{"aa": "kfjhgkdjfhgfdkhfdjg","bb": "ksdfhsdjhksdjh","cc": "fgdfgdfgdf", "dd":"gdfugydiuy6765888888"}'
```
### Subscribe Datahub
```
mqtt-bench subscribe --host 192.168.1.207 --port 1883 --topic "latency" --qos 0 --file output.txt --interval 2000
```
