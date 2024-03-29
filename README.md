# HBSIS OpenWeather Client

[![Build Status](https://travis-ci.org/jessequinn/hbsis.svg?branch=master)](https://travis-ci.org/jessequinn/hbsis)

The following web application consists of two backends (one api and another postgresql server) and the frontend. Both the api and frontend 
are programmed around Flask and python. 

The API backend contains the city, country and city id information for calling forecasts from OpenWeatherMap.org

The postgresql server contains user information and storage of city id.

A user registration has been created to allow individial sessions to be stored. Users can add or remove city forecast registrations and view upto 5 days of forecasts.

---
O seguinte aplicativo da web consiste em dois back-ends (uma api e outro servidor postgresql) e o front-end. Tanto a API como o frontend
são programados em torno do Flask e python.

O back-end da API contém as informações do código da cidade, país e cidade para chamar as previsões do OpenWeatherMap.org

O servidor postgresql contém informações do usuário e armazenamento do ID da cidade.

Um registro de usuário foi criado para permitir que sessões individuais sejam armazenadas. Os usuários podem adicionar ou remover registros de previsão da cidade e visualizar até cinco dias de previsões.

![](mockup.png)

Backend 1:

Flask serving sqlite based cities. (make_sqlite_db.py) converts city.list.json from openweathermap.org to sqlite.

To start the server simply run within the `backend_docker` folder :
```bash
python app.py 
```

To prepare container for Docker
```bash
docker build -t backend_docker .
docker run -d -p 5050:5050 backend_docker
```

Backend 2 (Postgresql Server):

Run the following commands within the `backend2_docker` folder to build and run a docker container with specific database settings.

database name: openweather
username: docker
password: docker

```bash
docker build -t postgresdocker .
docker run -dp 5432:5432 postgresdocker 
```

Flask (Frontend):

Set the os environment variables and run the frontend from `frontend_docker` folder. No `Dockerfile` has been setup.

```bash
export APP_MODE='config.DevelopmentConfig'
export DATABASE_URI='postgresql://docker:docker@localhost/openweather'
```
Run initially to prepare postgres db
```bash
# prepare db
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

Run the frontend
```bash
python manage.py runserver
```

to run tests
```bash
export APP_MODE='config.TestConfig'
export DATABASE_URI='postgresql://docker:docker@localhost/openweather'
python manage.py test
```

If there is a problem, please do not hesitate in contacting me.
