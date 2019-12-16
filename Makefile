build:
	docker build -t easyglobalmarket/mqtt-diatomic .
push:
	docker push easyglobalmarket/mqtt-diatomic	
run:
	docker run --name mqtt-diatomic --rm -e "IP=$(ip)" -e "PORT=$(port)"   easyglobalmarket/mqtt-diatomic	
stop:
	docker stop easyglobalmarket/mqtt-diatomic || true
	docker rm easyglobalmarket/mqtt-diatomic || true
	
	