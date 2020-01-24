run:
	docker run --rm -e "IP=192.168.1.207" -e "PORT=1883" -e "TOPIC=latency" -e "QOS=0" -e "INTERVAL=300" --name mqtt-subscriber -d  easyglobalmarket/mqtt-subscriber
	docker run --rm -e "IP=192.168.1.207" -e "PORT=1883" -e "TOPIC=latency" -e "ROUNDS=100" -e "INTERVAL=1" -e "CLIENTS=1" -e "COUNT=1000"  --name mqtt-latency -d easyglobalmarket/mqtt-latency
	sleep 200
	docker cp mqtt-subscriber:/output/res.txt c:\Users\asinatra\git\mqtt-benchmark\docker