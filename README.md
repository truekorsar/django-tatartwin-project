Django project, with which you can find 
a tatar word that is similar in spelling to a russian one.
 

## Installation for Linux(Ubuntu)
Besides Django itself, many other services are involved in the project. They are:
1. Redis - for caching tatar word search results, as message broker for Celery and Django Channels
2. Memcached - for storing sessions
3. Postgres - as database, also extensions 'fuzzystrmatch' and 'pg_trgm' are used
4. Celery - for sending emails and deleting inactive users with celerybeat
5. Docker - for deploying and as option to work with project locally

There are 2 ways you can start to with project: with Docker and without it
### Installation with Docker 
##### 1. Install Docker and Docker compose
##### 2. Download from Github
```
git clone https://github.com/truekorsar/django-tatartwin-project.git
```
##### 3. Then cd into project
```
cd ./django-tatartwin-project
```
##### 4. Prepare files for docker containers
In order for project to work via docker, there are 5 services declared in docker-compose.yml:
1. db-Postgres database
2. nginx - web server
3. web - Django project itself
4. redis - redis server
5. memcached - memcached server

Most of them (except Redis and Memcached) require special configuration files,
located in subdirectories in _`./docker-setup-project`_ and in _`./tatartwin/tatartwin`_ .
Files that have extension _.example_  contain sensitive info
(like credentials for email accounts and database, secret keys, etc). You can just delete _`.example`_ extension for these
files and move to next step, but keep in mind that features like sending mails won't work in this case. If it is a bother, see the
explanation of every file below.

In _`./docker-setup-project`_ we have 3 subdirectories: _`db`_, _`nginx`_ and _`web`_. They refer to
appropriate services from docker-compose.yml. Let's start from the first one.

In  _`./docker-setup-project/db`_ there are _`dbenv.env.example`_ and _`postgres_config.conf.example`_. 
They contain environment variables to create initial database and configuration information respectively.
More detailed information about these files can be found in _`https://hub.docker.com/_/postgres`_.
Everything will be fine if you just delete .example from their names.  
 
Similar situation in  _`./docker-setup-project/nginx`_ . We have _`default.conf.template.example`_ and _`nginx.env.example`_. 
First one is config file for nginx, while second one holds env variables for this file. 
Again, more detailed information about these files can be found in _`https://hub.docker.com/_/nginx`_.
Everything will be fine if you just delete .example from their names.

Now the moment where we stop for a while.
In  _`./docker-setup-project/web`_  we have something different: _`init-project.sh`_ and _`dbsetup.py`_.
Actually, they don't contain any sensitive information (that's why they don't have _`.example`_ at the end) and only intended to do 4 tasks:
create project database, populate it with info from _`./tatartwin/data`_, start celery workers and start Daphne server.
Process starts from _`init-project.sh`_, where in line 4 we execute _`dbsetup.py`_ to initialize database.
_`dbsetup.py`_ uses many environment variable in its work. _`POSTGRES_DB_NAME`_ is one that is called _`POSTGRES_DB`_ in _`dbenv.env.example`_ met above.
They must be equal. Other variables are Django project env variables, which located in  _`./tatartwin/tatartwin/settings.env.example`_ and will be described below.
Lines from 6-8 in _`init-project.sh`_ launch celery workers and start Daphne server.
Here you can leave everything as it is.

Finally, _`./tatartwin/tatartwin/settings.env.example`_ holds familiar to Django users setting variables. Some of them,
like _`SOCIAL_AUTH_VK_OAUTH2_KEY`_ or _`EMAIL_HOST_USER`_ are responsible for things like registration and logging in,
so unless you define your own values, this part of project will not work properly. Again, as described above, if it's not a problem
just delete .example extension and go to the next step. 

##### 5. Build containers and start them
```
sudo docker-compose up
```
This process can take a while and most likely fail if started at first time.
It can occur when we try to work from _`dbsetup.py`_ and _`init-project.sh`_ with database while it's not ready.
In this case you will see a corresponding message in console. Just do Ctrl+C and do ```sudo docker-compose up``` again.
Now, if you've left everything untouched in files from the 3rd step, you can type _`http://127.0.0.1:8000`_ in your browser and meet the index page.  

### Installation without Docker

Installation without Docker containers is pretty similar. One major difference is that you have to install Redis, Postgres and 
Memcached as ordinary programs.
 
##### 1. Download from Github
```
git clone https://github.com/truekorsar/django-tatartwin-project.git
```

##### 2. Then cd into project
```
cd ./django-tatartwin-project
```

Then you should probably change some variables in _`./tatartwin/tatartwin/settings.env.example`_ and delete .example at the end.
Most of these variables are described in Django docs.

##### 3. Create virtual environment and activate it
```
python3.8 -m venv venv && source ./venv/bin/activate
```
##### 4. Install all requirements
```
pip install -r requirements.txt
```

##### 5. Export environment variables
```
export $(grep -v '^#' ./tatartwin/tatartwin/settings.env | xargs -d '\n')
```

##### 6. Start Django server
```
python3.8 ./tatartwin/manage.py runserver
```
