## About
<p>Some information about this... :)</p>

## Download this repository
```git clone https://github.com/davidmonteiro03/website.git```

## Dependences
```sudo apt update```<br>
```sudo snap install docker```<br>
```sudo apt install -y python3 python3-pip python-is-python3```<br>
```pip install -r ./docker/srcs/requirements/website/tools/requirements.txt```<br><br>
You must create a .env file in ./docker/srcs/ directory and setup the following variables:
- PORT
- DJANGO_SUPERUSER_USERNAME
- DJANGO_SUPERUSER_EMAIL
- DJANGO_SUPERUSER_PASSWORD

## Execute with Docker
### build
Run ```make -S docker``` in the root of this repository
### up
Run ```make -S docker up``` in the root of this repository
### down
Run ```make -S docker down``` in the root of this repository
### clean
Run ```make -S docker clean``` in the root of this repository
### fclean
Run ```make -S docker fclean``` in the root of this repository
### re
Run ```make -S docker re``` in the root of this repository
### run
Open your browser and type ```http://localhost:<port>```<br>
> Note that ```<port>``` must be the ```$PORT``` value you setted up in .env file

## Execute in host machine
### setup
Run ```./setup.sh``` in the root of this repository
### run
Go to ```./docker/srcs/requirements/website/tools/website``` directory
Run ```python manage.py runserver 0.0.0.0:<port>```
Open your browser and type ```http://localhost:<port>```
> Note that ```<port>``` must be the port you want to allow to run this project
### clean
Run ```./clean.sh``` in the root of this repository
### info
Run ```./info.sh``` in the root of this repository
