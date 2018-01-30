# ezsetup

## Introduction

<!-- TODO: Describe what is ezsetup. Better have a logo. -->

## Installation

### From Source

0. (Optional, but recommended) Setup a virtual Python environment and activate it:
    ```bash
    python3 -m venv
    source venv/bin/activate
    ```
1. Install dependencies:
    - Python >= 3.6
    - Node >= 8.0
    - GNU make
    - Docker
1. Run `make install` to install requirements for the `frontend` and `api` projects;
2. Copy `.env.example` file to `.env` and fill in necessary fields;
3. Run `make run-api` to start the `api` server;
4. In another terminal session, run `make run-frontend` to start the `frontend` server.

## With Vagrant

1. Install VirtualBox and Vagrant;
2. (Optional) Copy `.env.example` file to `.env` and fill in necessary fields;
3. Run `vagrant up` in your project root directory;
4. You can file your credentials in the `.env` file in your project root directory.

## With Docker

<!-- TODO -->

## Contributing

### Coding Styles
<!-- TODO: Use linter to enforce code styles -->
- **HTML & CSS**: [Code Guide by @mdo](http://codeguide.co)
- **JavaScript**: [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- **Python**: [PEP 8](https://www.python.org/dev/peps/pep-0008/)

### Developing and Deploying
- **Git Commit Style**: [AngularJS Git Commit Message Conventions](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit)
- **Veriosning**: [Semantic Versioning 2.0.0](https://semver.org/)
