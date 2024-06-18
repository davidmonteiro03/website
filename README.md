# Website
## About
<p>Some information about this... :)</p>

## Execute with Docker
### Dependences
```sudo snap install docker```
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

## Execute in host machine
### Dependences
```sudo apt update```<br>
```sudo apt install -y python3 python3-pip python-is-python3```<br>
```pip install -r ./docker/srcs/requirements/website/tools/requirements.txt```
