#!/bin/bash

echo "******* mqttprobe: starting entrypoint.sh ******"

source /mqtt-functional-probe/config.cfg

echo "ip = $IP"
echo "port = $PORT"

echo "******* mqttprobe: executing benchmark *******"

	
while true
do
	for k in $(jq -r '.[]' <<< "$BULK_DATA"); do
		echo $k
		mqtt-bench publish --host $IP --port $PORT --topic $topic  --message $k --randomize-payload-value True --payload 
	done
	sleep 1
done

