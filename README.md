## Development status
<p>This project is actively being developed. We are currently working on improving performance and adding new features to enhance user experience. Feel free to check out our recent commits and join the discussion in the issues section!

## Download this repository
Run `git clone https://github.com/davidmonteiro03/website.git` in your terminal

## Dependences
<p>Run <code>sudo apt update</code> in your terminal</p>
<p>Run `sudo snap install docker` in your terminal</p>
<p>Run `sudo apt install -y make python3 python3-pip python-is-python3` in your terminal</p>
<p>Run `pip install -r ./docker/srcs/requirements/website/tools/requirements.txt` in your terminal</p>
<p>Create a `.env` file in `./docker/srcs/` directory and setup the following variables:</p>
<p>- `PORT`
- `DJANGO_SUPERUSER_USERNAME`
- `DJANGO_SUPERUSER_EMAIL`
- `DJANGO_SUPERUSER_PASSWORD`</p>

## Execute with Docker
### build
Run `make -C docker` in the root of this repository
### up
Run `make -C docker up` in the root of this repository
### down
Run `make -C docker down` in the root of this repository
### clean
Run `make -C docker clean` in the root of this repository
### fclean
Run `make -C docker fclean` in the root of this repository
### re
Run `make -C docker re` in the root of this repository
### run
Open your browser and type `http://localhost:<port>`<br>
> Note that `<port>` must be the `$PORT` value you setted up in `.env` file

## Execute in host machine
### setup
Run `./setup.sh` in the root of this repository
### clean
Run `./clean.sh` in the root of this repository
### info
Run `./info.sh` in the root of this repository
### run
Go to `./docker/srcs/requirements/website/tools/website` directory<br>
Run `python manage.py runserver 0.0.0.0:<port>`<br>
Open your browser and type `http://localhost:<port>`<br>
> Note that `<port>` must be the port you want to allow to run this project
