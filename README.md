## About
<p>

Some information about this... :)

</p>

## Download this repository
<p>

Run `git clone https://github.com/davidmonteiro03/website.git` in your terminal

</p>

## Dependences
<p>

Run `sudo apt update` in your terminal

</p>
<p>

Run `sudo snap install docker` in your terminal

</p>
<p>

Run `sudo apt install -y make python3 python3-pip python-is-python3` in your terminal

</p>
<p>

Run `pip install -r ./docker/srcs/requirements/website/tools/requirements.txt` in your terminal

</p>
<p>

Create a `.env` file in `./docker/srcs/` directory and setup the following variables:
- `PORT`
- `DJANGO_SUPERUSER_USERNAME`
- `DJANGO_SUPERUSER_EMAIL`
- `DJANGO_SUPERUSER_PASSWORD`

</p>

## Execute with Docker
### build
<p>

Run `make -C docker` in the root of this repository

</p>

### up
<p>

Run `make -C docker up` in the root of this repository

</p>

### down
<p>

Run `make -C docker down` in the root of this repository

</p>

### clean
<p>

Run `make -C docker clean` in the root of this repository

</p>

### fclean
<p>

Run `make -C docker fclean` in the root of this repository

</p>

### re
<p>

Run `make -C docker re` in the root of this repository

</p>

### run
<p>

Open your browser and type `http://localhost:<port>`
> Note that `<port>` must be the `PORT` value you setted up in `.env` file

</p>

## Execute in host machine
### setup
<p>

Run `./setup.sh` in the root of this repository

</p>

### clean
<p>

Run `./clean.sh` in the root of this repository

</p>

### info
<p>

Run `./info.sh` in the root of this repository

</p>

### run
<p>

Go to `./docker/srcs/requirements/website/tools/website` directory

</p>
Run `python manage.py runserver 0.0.0.0:<port>`

</p>

Open your browser and type `http://localhost:<port>`
> Note that `<port>` must be the port you want to allow to run this project

</p>
