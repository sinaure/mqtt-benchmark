# MQTT Benchmark Client for Python
無聊拿來測試用的簡單 MQTT 測試客戶端。


## Quick
首先 clone 該專案到自己環境：
```sh
$ git clone https://github.com/imac-cloud/mqtt-benchmark.git
```

進入到目錄，之後透過 ```pip``` 或者 ```setup.py``` 安裝：
```sh
$ cd mqtt-benchmark
$ pip install .
```
> 若是使用```setup.py```則使用以下方式：
```sh
$ python setup.py install
```

### Publish
簡單的 Publish 可以使用以下指令來執行：
```sh
$ mqtt-bench publish --host 192.168.99.100 --port 1883 \
--qos 0 --thread-num 0 \
--topic "Test" \
--message "I'm test."
```
> ```--thread-num```若```>=0```的話，會每秒 Publish 一次。

### Subscribe
簡單的 Subscribe 可以使用以下指令來執行：
```sh
$ mqtt-bench subscribe --host 192.168.99.100 --port 1883 --topic "test" --qos 0
```