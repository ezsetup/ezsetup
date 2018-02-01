container_name = ezsetup_pg
shell:
	psql -h localhost -p 5433 -U ${POSTGRES_USER} -w
	
build:
	docker build -t registry.gitlab.com/promises/pg:${PG_IMAGE_VERSION} . && \
		docker push registry.gitlab.com/promises/pg:${PG_IMAGE_VERSION}

build-dev:
	# Build a public docker image for easying development and testing
	# Make sure this image doesn't contain any sensitive data
	docker build -t nguyendv/ezsetup-pg-dev:latest . && \
		docker push nguyendv/ezsetup-pg-dev:latest

run:
	echo ${POSTGRES_USER}; \
	docker stop ${container_name} && \
	docker rm ${container_name}; \
	docker run -d -p 5433:5432 --name ${container_name} --restart=unless-stopped -e POSTGRES_USER=${POSTGRES_USER} -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} -e PGDATA=${PGDATA} -v $(CURDIR)/pgdata:${PGDATA} registry.gitlab.com/promises/pg:${PG_IMAGE_VERSION}

dump:
	echo ${POSTGRES_PASSWORD}
	pg_dump -U ${POSTGRES_USER} -h localhost -p 5433 -d ${POSTGRES_USER} > 0000-`date +%Y-%m-%d`.sql

logs:
	docker logs -f ${container_name}
