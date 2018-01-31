POSTGRES_PORT = 5441
REDIS_PORT = 6381

redis-container = ezsetup-redis-test
postgres-container = ezsetup-pg-test

run:
	source .env; \
	pipenv run python app.py

start-test-containers:
	# start test redis
	docker run --name ${redis-container} --restart=unless-stopped -d -p ${REDIS_PORT}:6379 redis:4

	# start test db
	docker run -d -p ${POSTGRES_PORT}:5432 --name ${postgres-container} --restart=unless-stopped -e POSTGRES_USER=${POSTGRES_USER} -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} -e PGDATA=${PGDATA} -v $(CURDIR)/pgtestdata:${PGDATA} registry.gitlab.com/promises/pg:2018.01.12

run-tests:
	# run tests
	pipenv run mypy --ignore-missing-imports app.py
	pipenv run mypy --ignore-missing-imports tests
	PYTHONPATH=. pipenv run pytest

clean-test-containers:
	# drop test db
	docker stop ${postgres-container} ;\
	docker rm ${postgres-container};\
	rm -rf $(CURDIR)/pgtestdata;\
	
	# drop test redis
	docker stop ${redis-container}; \
	docker rm ${redis-container};

test:
	$(MAKE) clean-test-containers;\
	$(MAKE) start-test-containers;\
	sleep 10;\
	$(MAKE) run-tests

