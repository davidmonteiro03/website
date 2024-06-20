## About
<p>

Welcome to the repository! This document provides comprehensive instructions for setting up, building, and running the project both via Docker and directly on your host machine.

</p>

## Download this repository
<p>To clone this repository, execute the following command in your terminal:</p>

`git clone https://github.com/davidmonteiro03/website.git`

## Dependences

<p>Before running the project, ensure you have the necessary dependencies installed by executing the following commands in your terminal:</p>

1. Update your package list:
   - `sudo apt update`
2. Install Docker using Snap: `sudo snap install docker`
3. Install this required packages: `sudo apt install -y make python3 python3-pip python-is-python3`
4. Install this Python dependencies: `pip install -r ./docker/srcs/requirements/website/tools/requirements.txt`

<p>

Additionally, create a `.env` file in the `./docker/srcs/` directory with the following variables:

</p>

`PORT`
`DJANGO_SUPERUSER_USERNAME`
`DJANGO_SUPERUSER_EMAIL`
`DJANGO_SUPERUSER_PASSWORD`

## Execute with Docker
### build
<p>

Execute `make -C docker` in the root of this repository

</p>

### up
<p>

Execute `make -C docker up` in the root of this repository

</p>

### down
<p>

Execute `make -C docker down` in the root of this repository

</p>

### clean
<p>

Execute `make -C docker clean` in the root of this repository

</p>

### fclean
<p>

Execute `make -C docker fclean` in the root of this repository

</p>

### re
<p>

Execute `make -C docker re` in the root of this repository

</p>

### run
<p>

Open your browser and type `http://localhost:<port>`
> Note that `<port>` must be the `PORT` value you setted up in `.env` file

</p>

## Execute in host machine
### setup
<p>

Execute `./setup.sh` in the root of this repository

</p>

### clean
<p>

Execute `./clean.sh` in the root of this repository

</p>

### info
<p>

Execute `./info.sh` in the root of this repository

</p>

### run
<p>

Navigate to `./docker/srcs/requirements/website/tools/website` directory

</p>
<p>

Execute `python manage.py runserver 0.0.0.0:<port>`

</p>
<p>

Open your browser and type `http://localhost:<port>`
> Note that `<port>` must be the port you want to allow to run this project

</p>
