## Project Foodgram

Foodgram - is a simple service with cooking recipes. Allows you to add and publish recipes, save favorites, and download a shopping list for selected recipes. There is a subscription for authors.

The documentation describes all possible requests to the API and the structure of the expected responses. Access rights levels are specified for each request.

### Technology Stack:

Python, Django, Django Rest Framework, Docker, Gunicorn, NGINX, PostgreSQL, Continuous Integration, Continuous Deployment

### Running a project on a remote server:

- Install Docker and Docker Compose on the server:

```
sudo apt install curl                                   # installing a utility for downloading files
curl -fsSL https://get.docker.com -o get-docker.sh      # download installation script
sh get-docker.sh                                        # start the script
sudo apt-get install docker-compose-plugin              # last version of docker compose
```

- Copy the files docker-compose.yml, nginx.conf from the infra folder and the docs folder to the server on the same level as the foodgram folder (manually or via ssh), for example:

```
scp docker-compose.yml nginx.conf username@IP:/home/username/   # username - имя пользователя на сервере
                                                                # IP - публичный IP сервера
```

- To work with GitHub Actions, you need to create environment variables in the repository in the Secrets > Actions section:
```
SECRET_KEY              # secret key of the Django project
DOCKER_PASSWORD         # password from Docker Hub
DOCKER_USERNAME         # login of Docker Hub
HOST                    # puplic server IP
USER                    # username on the server
PASSPHRASE              # *if ssh-key is protected with password
SSH_KEY                 # private ssh-key

DB_ENGINE               # django.db.backends.postgresql
DB_NAME                 # postgres
POSTGRES_USER           # postgres
POSTGRES_PASSWORD       # postgres
DB_HOST                 # db
DB_PORT                 # 5432 (default port)
```

- Download the latest versions of containers from DockerHub, run the command on the server
*(versions of the "docker compose" or "docker-compose" commands differ depending on the version of Docker Compose installed):*
```
sudo docker compose -f docker-compose.production.yml pull
```

- Create and run Docker containers, run the command on the server
*(versions of the "docker compose" or "docker-compose" commands differ depending on the version of Docker Compose installed):*
```
sudo docker compose -f docker-compose.production.yml up -d
```

- After a successful build, run migrations:
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
```

- Create superuser:
```
sudo docker compose exec backend python manage.py createsuperuser
```

- Collect static:
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
```

- Copy static to backend container:
```
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/static/. /backend_static/static/
```

- Fill the database with content from a file ingredients.json:
```
sudo docker compose exec backend python manage.py shell
from scripts.load_csv import load_ingredients
load_ingredients('data/ingredients.csv')
```

- To stop Docker containers:
```
sudo docker compose down -v      # with deleting containers
sudo docker compose stop         # without deleting
```

### Running a project on a local machine:

- Clone repo:
```
git@github.com:bananapowerchicken/foodgram-project-react.git
```

- n the infra file directory, create a .env file and fill it with your data according to the example below:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY='secret Django key'
```

- Create and run Docker containers, sequentially execute commands to create migrations, collect statics,
creating a superuser as above.
```
docker-compose -f docker-compose.yml up -d
```


- After launch, the project will be available at: [http://localhost/](http://localhost/)


- Documentation will be available at: [http://localhost/api/docs/](http://localhost/api/docs/)
