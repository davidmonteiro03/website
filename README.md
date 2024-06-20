## About
<p>Some information about this... :)</p>

## Download this repository
<p>Run <code>git clone https://github.com/davidmonteiro03/website.git</code> in your terminal</p>

## Dependences
<p>Run <code>sudo apt update</code> in your terminal</p>
<p>Run <code>sudo snap install docker</code> in your terminal</p>
<p>Run <code>sudo apt install -y make python3 python3-pip python-is-python3</code> in your terminal</p>
<p>Run <code>pip install -r ./docker/srcs/requirements/website/tools/requirements.txt</code> in your terminal</p>
<p>Create a <code>.env</code> file in <code>./docker/srcs/</code> directory and setup the following variables:

- <code>PORT</code>
- <code>DJANGO_SUPERUSER_USERNAME</code>
- <code>DJANGO_SUPERUSER_EMAIL</code>
- <code>DJANGO_SUPERUSER_PASSWORD</code>

</p>

## Execute with Docker
### build
<p>Run <code>make -C docker</code> in the root of this repository</p>

### up
<p>Run <code>make -C docker up</code> in the root of this repository</p>

### down
<p>Run <code>make -C docker down</code> in the root of this repository</p>

### clean
<p>Run <code>make -C docker clean</code> in the root of this repository</p>

### fclean
<p>Run <code>make -C docker fclean</code> in the root of this repository</p>

### re
<p>Run <code>make -C docker re</code> in the root of this repository</p>

### run
<p>Open your browser and type <code>http://localhost:&lt;port&gt;</code>

> Note that <code>&lt;port&gt;</code> must be the <code>$PORT</code> value you setted up in <code>.env</code> file

</p>

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
