build-server:
	docker-compose build app
server:
	docker-compose run -d app
stop-server:
	docker-compose stop app
rm-server:
	docker-compose rm app
run: build-server server
clear: stop-server rm-server
