## Проект Foodgram

Foodgram - это простой сервис с кулинарными рецептами. Позволяет  добавлять и публиковать рецепты, сохранять избранные, а также скачивать список покупок для выбранных рецептов. Есть подписка на авторов.

Проект доступен по [адресу](http://51.250.28.193/)

Документация к API доступна [здесь](http://51.250.28.193/api/docs/)

В документации описаны все возможные запросы к API и структура ожидаемых ответов. Для каждого запроса указаны уровни прав доступа.

### Использованные Технологии:

Python, Django, Django Rest Framework, Docker, Gunicorn, NGINX, PostgreSQL, Continuous Integration, Continuous Deployment

### Данные администратора на удаленном сервере для ревью

email: admin1@yap.com
password: adminpassword1

### Запуск проекта на удаленном сервере:

- Установить на сервере Docker и  Docker Compose:

```
sudo apt install curl                                   # установка утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh      # скачать скрипт для установки
sh get-docker.sh                                        # запуск скрипта
sudo apt-get install docker-compose-plugin              # последняя версия docker compose
```

- Скопировать на сервер файлы docker-compose.yml, nginx.conf из папки infra и папку docs на один уровень с папкой foodgram (вручную или через ssh), например:

```
scp docker-compose.yml nginx.conf username@IP:/home/username/   # username - имя пользователя на сервере
                                                                # IP - публичный IP сервера
```

- Для работы с GitHub Actions необходимо в репозитории в разделе Secrets > Actions создать переменные окружения:
```
SECRET_KEY              # секретный ключ Django проекта
DOCKER_PASSWORD         # пароль от Docker Hub
DOCKER_USERNAME         # логин Docker Hub
HOST                    # публичный IP сервера
USER                    # имя пользователя на сервере
PASSPHRASE              # *если ssh-ключ защищен паролем
SSH_KEY                 # приватный ssh-ключ

DB_ENGINE               # django.db.backends.postgresql
DB_NAME                 # postgres
POSTGRES_USER           # postgres
POSTGRES_PASSWORD       # postgres
DB_HOST                 # db
DB_PORT                 # 5432 (порт по умолчанию)
```

- Скачать последние вресии контейнеров с  DockerHub, выполнить команду на сервере
*(версии команд "docker compose" или "docker-compose" отличаются в зависимости от установленной версии Docker Compose):*
```
sudo docker compose -f docker-compose.production.yml pull
```

- Создать и запустить контейнеры Docker, выполнить команду на сервере
*(версии команд "docker compose" или "docker-compose" отличаются в зависимости от установленной версии Docker Compose):*
```
sudo docker compose -f docker-compose.production.yml up -d
```

- После успешной сборки выполнить миграции:
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
```

- Создать суперпользователя:
```
sudo docker compose exec backend python manage.py createsuperuser
```

- Собрать статику:
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
```

- Скопировать статику в контейнер backend:
```
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/static/. /backend_static/static/
```

- Наполнить базу данных содержимым из файла ingredients.json:
```
sudo docker compose exec backend python manage.py shell
from scripts.load_csv import load_ingredients
load_ingredients('data/ingredients.csv')
```

- Для остановки контейнеров Docker:
```
sudo docker compose down -v      # с их удалением
sudo docker compose stop         # без удаления
```

### Запуск проекта на локальной машине:

- Клонировать репозиторий:
```
git@github.com:bananapowerchicken/foodgram-project-react.git
```

- В директории infra файл создать файл .env и заполнить своими данными по нижеприведенному примеру:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY='секретный ключ Django'
```

- Создать и запустить контейнеры Docker, последовательно выполнить команды по созданию миграций, сбору статики, 
созданию суперпользователя, как указано выше.
```
docker-compose -f docker-compose.yml up -d
```


- После запуска проект будут доступен по адресу: [http://localhost/](http://localhost/)


- Документация будет доступна по адресу: [http://localhost/api/docs/](http://localhost/api/docs/)
