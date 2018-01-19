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
0. (Optional) Setup a virtual Python environment and activate it:
```
python3 -m venv <choose a name> # for instance, I often set it as "venv"
source venv/bin/activate
```
1. Install GNU make
2. Run `make install`: this command installs all requirements for the `frontend` and `api` projects
3. Install `docker`
4. Run `make run` to run the `api`'s development server and `frontend`
5. Open `http://localhost:8000`

## With Vagrant
