## About
<p>Something to describe the project (I don't know yet how to describe this).</p>

## Repository Download
<p>To clone this repository, run the following command in your terminal:</p>

`git clone https://github.com/davidmonteiro03/website.git`

## Dependencies
<p>Before running the project, ensure you have the necessary dependencies installed by executing the following commands in your terminal:</p>

1. Update your package list:
   - `sudo apt update`

2. Install Docker using Snap:
   - `sudo snap install docker`

3. Install the required packages:
   - `sudo apt install -y make python3 python3-pip python-is-python3`

4. Install Python dependencies:
   - `pip install -r ./docker/srcs/requirements/website/tools/requirements.txt`

5. Create a `.env` file in the `./docker/srcs/` directory with the following variables:
   - `PORT`
   - `DJANGO_SUPERUSER_USERNAME`
   - `DJANGO_SUPERUSER_EMAIL`
   - `DJANGO_SUPERUSER_PASSWORD`

## Running with Docker
### Build and Start
<p>To build and start the Docker environment, run:</p>

`make -C docker`

### Build
<p>To build the Docker images only, run:</p>

`make -C docker build`

### Start
<p>To start the Docker containers, run:</p>

`make -C docker up`

### Stop
<p>To stop the Docker containers, run:</p>

`make -C docker down`

### Restart
<p>To restart the Docker containers, run:</p>

`make -C docker restart`

### Clean
<p>To clean up containers and associated volumes, run:</p>

`make -C docker clean`

### Full Clean
<p>To perform a full cleanup, removing all Docker artifacts, run:</p>

`make -C docker fclean`

### Re-run
<p>To stop and start the Docker containers again, run:</p>

`make -C docker rerun`

### Rebuild
<p>To rebuild the Docker environment from scratch, run:</p>

`make -C docker re`

### Running the Application
<p>After starting the Docker containers, open your browser and navigate to:</p>

`http://localhost:<port>`

<p>

Ensure that `<port>` matches the `PORT` value specified in your `.env` file.

</p>

## Running on the Host Machine
### Setup
<p>To set up the project directly on your host machine, execute the setup script from the root of the repository:<p>

`./setup.sh`

### Clean
<p>To clean the environment, execute:</p>

`./clean.sh`

### Information
<p>To display project information, execute:</p>

`./info.sh`

### Running the Application
<p>To run the project directly on your host machine, navigate to the application directory:</p>

`cd ./docker/srcs/requirements/website/tools/website`

<p>Then, execute the following command to start the Django development server:</p>

`python manage.py runserver 0.0.0.0:<port>`

<p>Open your browser and navigate to:</p>

`http://localhost:<port>`

<p>

Make sure `<port>` is set to the desired port number for running the project.

</p>
