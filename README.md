<div align="center">

# Travel Management

<img src="/readme/banner.png" width="56%">

![VERSION: V0.2.0 (shields.io)](https://img.shields.io/badge/version-v0.2.0-1ED760?&style=for-the-badge&logo=qgis&logoColor=white)
![DJANGO (shields.io)](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![REACT (shields.io)](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![JAVA SWING (shields.io)](https://img.shields.io/badge/Java%20Swing-0074BD?&style=for-the-badge&logo=java&logoColor=EA2D2E)
![POSTGRESQL (shields.io)](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![ANT DESIGN (shields.io)](https://img.shields.io/badge/Ant%20Design-1890FF?style=for-the-badge&logo=antdesign&logoColor=white)
![DOCKER (shields.io)](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![GITPOD (shields.io)](https://img.shields.io/badge/Gitpod-000000?style=for-the-badge&logo=gitpod&logoColor=#FFAE33)

</div>

---

- [Introduction](#introduction)
- [Front-end](#front-end)
- [Back-end](#back-end)
- [Desktop app](#desktop-app)
- [Document](#document)
- [Try it now](#try-it-now)

---

## Introduction

## Front-end

## Back-end

Back-end using **Django** for building REST API

### How to run back-end
**1. Di chuyển đến thư mục** `\QuanLyTourDuLich\backend\travel_management` 

**2. Build docker image**

```shell
docker build -t pl_backend .
```

*hoặc*

```shell
make build
```


**3. Run server bằng docker-compose**

```shell
docker-compose -p travel_management up
```

*hoặc*

```shell
make up
```

**4. Khởi tạo Database**

```shell
docker exec -it pl_backend pipenv run python3 manage.py migrate
```

*hoặc*

```shell
make init
```

---

### Makefile info

| rule    | command                                                                 | description                        | note                             |
|---------|-------------------------------------------------------------------------|------------------------------------|----------------------------------|
| build   | docker build -t pl_backend .                                            | build image for Django app         |                                  |
| up      | docker-compose -p travel_management up                                  | start apps                         |                                  |
| down    | docker-compose -p travel_management down                                | down apps                          |                                  |
| restart | docker-compose -p travel_management down                                | restart apps                       |                                  |
|         | docker-compose -p travel_management up                                  |                                    |                                  |
| init    | docker exec -it pl_backend pipenv run python3 manage.py migrate         | migrate new Django's migration(s)  |                                  |
|         | docker exec -it pl_backend pipenv run python3 manage.py init_super_user | init super user account            |                                  |
|         | docker exec -it pl_backend pipenv run python3 manage.py init_tour_data  | init tour data                     |                                  |
|         | docker exec -it pl_backend pipenv run python3 manage.py init_group_data | init group data                    |                                  |
| migrate | docker exec -it pl_backend pipenv run python3 manage.py migrate         | migrate new Django's migration(s)  |                                  |
| install | docker exec -it pl_backend pipenv install $(package)                    | install new package(s) with pipenv | rebuild image after installation |

---

### Account

| type                | username | password  | note                                               |
|---------------------|----------|-----------|----------------------------------------------------|
| admin site (Django) | admin    | 12345678  |                                                    |
| postgreSQL          | pl_user  | asd123!@# | host: localhost:5433 \| DB name: travel_management |

> Các environment variable được định nghĩa ở dev.env

## Desktop app

## Document

## Try it now
