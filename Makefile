redis_container=ezsetup_redis
pg_container=ezsetup_pg

install:
	cd api && pip install pipenv && pipenv --python 3.6 && pipenv install -d
	cd frontend && npm install

install-production:
	cd api && pip install pipenv && pipenv --python 3.6 && pipenv install
	cd frontend && npm install --production

run-api: run-dockers
	source .env && cd api && pipenv run python app.py &

run-frontend:
	cd frontend && npm run dev

run-dockers:
	[[ $$(docker ps -f "name=${redis_container}" --format '{{.Names}}') == ${redis_container} ]] || \
	docker run --name ${redis_container} --restart=unless-stopped -d -p ${REDIS_PORT}:6379 redis:3.2

	[[ $$(docker ps -f "name=${pg_container}" --format '{{.Names}}') == ${pg_container} ]] || \
	docker run -d -p ${POSTGRES_PORT}:5432 --name ${pg_container} --restart=unless-stopped -e POSTGRES_USER=${POSTGRES_USER} -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} -e PGDATA=${PGDATA} -v $(CURDIR)/pgdata:${PGDATA} nguyendv/ezsetup-pg-dev:latest

