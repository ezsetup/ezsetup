redis_container=ezsetup_redis
pg_container=ezsetup_pg

install:
	pip install -r api/requirements-dev.txt
	pip install -r api/requirements-test.txt

	cd frontend && npm install


run-api: run-dockers
	source .env && cd api && python app.py &

run-frontend:
	cd frontend && npm run dev

run-dockers:
	[[ $$(docker ps -f "name=${redis_container}" --format '{{.Names}}') == ${redis_container} ]] || \
	docker run --name ${redis_container} --restart=unless-stopped -d -p ${REDIS_PORT}:6379 redis:3.2

	[[ $$(docker ps -f "name=${pg_container}" --format '{{.Names}}') == ${pg_container} ]] || \
	docker run -d -p ${POSTGRES_PORT}:5432 --name ${pg_container} --restart=unless-stopped -e POSTGRES_USER=${POSTGRES_USER} -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} -e PGDATA=${PGDATA} -v $(CURDIR)/pgdata:${PGDATA} registry.gitlab.com/promises/pg:${PG_IMAGE_VERSION}

