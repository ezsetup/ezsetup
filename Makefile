include .env
export

install:
	cd api && pip install pipenv && pipenv --python 3.6 && pipenv install -d
	cd frontend && npm install

install-production:
	cd api && pip install pipenv && pipenv --python 3.6 && pipenv install
	cd frontend && npm install --production

run-api:
	cd api && pipenv run python app.py

run-worker:
	cd api && pipenv run rq worker -c backgroundjobs.settings

run-frontend:
	cd frontend && npm run dev

test:
	cd api && pipenv run mypy --ignore-missing-imports app.py
	cd api && pipenv run mypy --ignore-missing-imports tests
	cd api && PYTHONPATH=. pipenv run pytest

db-shell:
	PGPASSWORD=${POSTGRES_PASSWORD} psql -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -U ${POSTGRES_USER} -w

db-dump:
	PGPASSWORD=${POSTGRES_PASSWORD} pg_dump -U ${POSTGRES_USER} -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} \
	-d ${POSTGRES_USER}
