Monorepo for ezsetup project

# Why monorepo?
Previously, EZSetup is structured as a group of repositories, each for one component of EZSetup project. However, to move EZSetup to Github, I have to restructure it as a big monorepo. The reasons are:

1. There's no way I can create a private organization with my current Github plan. This feature costs $9 per member.
2. It's easier to do integratoin testing in a monorepo.
3. It's easier to set up CI/CD pipelines from one repo.
2. It's easier to sync all components in a monorepo: once a commit passes all test, we can be confident that all components are working well.

# How to setup development environment
## For Unix machines without Vagrant
*Requirements*
- Python >= 3.5
- Node >= 8.0
*Steps*
0. (Optional, but recommended) Setup a virtual Python environment and activate it:
```
python3 -m venv <choose a name> # for instance, I often set it as "venv"
source venv/bin/activate
```
1. Install GNU make
2. Run `make install`: this command installs all requirements for the `frontend` and `api` projects
3. Install `docker`
4. Create .env file with below format. (Don't commit this file to source version control)
5. Run `make run-api` to run the `api`'s development server
6. In another terminal tab or windows, run `make run-frontend` to run the `frontend`

**.env**
```
export REDIS_HOST=localhost
export REDIS_PORT=6378
export REDIS_TOKEN_DB=1

export POSTGRES_USER=ezsetup
export POSTGRES_PASSWORD=<enter your secret password>
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5433
export POSTGRES_POOL_MIN_CONN=10
export POSTGRES_POOL_MAX_CONN=100
export PGDATA=/var/lib/postgresql/data/pgdata
export 12 export PG_IMAGE_VERSION=2018.01.12 <or other version>

SENTRY_DSN=<enter SENTRY_DSN. Ask Dung for his sentry_dsn, or register a new one at sentry.io>
export SENTRY_DSN
```

## With Vagrant
