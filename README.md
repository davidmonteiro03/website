## About
<p>Something to describe the project (I don't know yet how to describe this).</p>

## Repository Download
<p>To clone this repository, execute the following command in your terminal:</p>

`git clone https://github.com/davidmonteiro03/website.git`

## Dependencies
<p>Before running the project, ensure you have the necessary dependencies installed by executing the following commands in your terminal:</p>

1. Update your package list:
   - `sudo apt update`
2. Install Docker using Snap:
   - `sudo snap install docker`
3. Install this required packages:
   - `sudo apt install -y make python3 python3-pip python-is-python3`
4. Install this Python dependencies:
   - `pip install -r ./docker/srcs/requirements/website/tools/requirements.txt`
5. Create a `.env` file in the `./docker/srcs/` directory with the following variables:
   - `PORT`
   - `DJANGO_SUPERUSER_USERNAME`
   - `DJANGO_SUPERUSER_EMAIL`
   - `DJANGO_SUPERUSER_PASSWORD`

## Running with Docker
### All
<p>To build the Docker environment, run the following command from the root of the repository:</p>

`make -C docker`

### Build
<p>To build the Docker environment, run the following command from the root of the repository:</p>

`make -C docker build`

### Up
<p>To start the Docker containers, execute:</p>

`make -C docker up`

### Down
<p>To stop the Docker containers, execute:</p>

`make -C docker down`

### Clean
<p>To clean up intermediate files and containers, execute:</p>

`make -C docker clean`

### Full Clean
<p>To perform a thorough clean-up, removing all Docker artifacts, execute:</p>

`make -C docker fclean`

### Rebuild
<p>To rebuild the Docker environment from scratch, execute:</p>

`make -C docker rebuild`

### Running the Application
<p>After starting the Docker containers, open your browser and navigate to:</p>

`http://localhost:<port>`

<p>

Ensure that `<port>` matches the `PORT` value specified in your `.env` file.

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
