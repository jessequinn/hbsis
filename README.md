# hbsis_weather_cliente
teste_dev_hercules

Backend:

Flask serving sqlite based cities. (make_sqlite_db.py) converts city.list.json from openweathermap.org to sqlite.

To test that the Flask app is working
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

To prepare container for Docker
```bash
docker build -t backend_docker .
```

run container in background with port 4050 open
```bash
docker run -d -p 4050:5050 backend_docker
```

Postgres Server (Backend 2):

run the following commands to build and run a docker container with specific database settings.

database name: openweather
username: docker
password: docker

```bash
docker build -t postgresdocker .

docker run -dp 5432:5432 postgresdocker 
```

Flask (Frontend):

set the os environment variables

```bash
export APP_MODE='config.DevelopmentConfig'
export DATABASE_URI='postgresql://docker:docker@localhost/openweather'
python app.py
```
