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
```make -S docker```
### up
```make -S docker up```
### down
```make -S docker down```
### clean
```make -S docker clean```
### fclean
```make -S docker fclean```
### re
```make -S docker re```
### run
Open your browser and type ```http://localhost:$PORT```
> Note that $PORT must be the value you setted up in .env file

## Execute in host machine
### setup
```./setup.sh```
### run
```cd ./docker/srcs/requirements/website/tools/website && python manage.py runserver <host>:<port>```
### clean
```./clean.sh```
### info
```./info.sh```
