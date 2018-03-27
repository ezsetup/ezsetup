[![CircleCI](https://circleci.com/gh/ezsetup/ezsetup.svg?style=svg)](https://circleci.com/gh/ezsetup/ezsetup)

# ezsetup

## Introduction

<!-- TODO: Describe what is ezsetup. Better have a logo. -->

## Dev Installation

### From Source

1. Install dependencies:
    - Python >= 3.6
    - Node >= 8.0
    - GNU make
    - PostgreSQL >= 9.6
    - Redis >= 3.2
    - pipenv
2. Copy `.env.example` file to `.env` and fill in necessary fields, and load environment variables by:

    ```bash
    source .env
    ```
3. Initialize database using migration files under `api/database/migrations`

    ```bash
    sudo su postgres -c "psql -c \"CREATE ROLE ${POSTGRES_USER} WITH SUPERUSER CREATEDB CREATEROLE LOGIN ENCRYPTED PASSWORD '${POSTGRES_PASSWORD}';\""
    sudo su postgres -c "createdb ${POSTGRES_USER}"
    sudo su postgres -c "cat api/database/migrations/*.sql | psql -d ${POSTGRES_USER}"
    ```
4. Run `make install` to install requirements for the `frontend` and `api` projects;
5. Run `make run-worker` to start a redis-queue worker
6. Run `make run-api` to start the `api` server, or `make run-frontend` to start the `frontend` server. Run `make test` 
to execute tests.

## With Vagrant

1. Install VirtualBox and Vagrant;
2. Copy `.env.example` file to `.env` and fill in necessary fields;
3. Run `vagrant up` from your project root directory (Windows users need to run this command as administrator to avoid 
the symlink error);

## With Docker

1. Install Docker and docker-compose;
2. Copy `.env.example` file to `.env` and fill in necessary fields, and load environment variables by:

    ```bash
    source .env
    ```
3. Run `docker-compose up` from your project directory to bring up services. To execute tests, run

    ```bash
    docker-compose -f docker-compose.test.yml up --abort-on-container-exit
    ```

## Contributing

### Coding Styles
<!-- TODO: Use linter to enforce code styles -->
- **HTML & CSS**: [Code Guide by @mdo](http://codeguide.co)
- **JavaScript**: [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- **Python**: [PEP 8](https://www.python.org/dev/peps/pep-0008/)

### Developing and Deploying
- **API Style**: [GitHub API v3](https://developer.github.com/v3/)
- **Git Commit Style**: [AngularJS Git Commit Message Conventions](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit)
- **Veriosning**: [Semantic Versioning 2.0.0](https://semver.org/)

#### For the UALR internal version only
Code for the UALR internal only can only be pushed to the branch "UALR-INTERNAL-ONLY"
