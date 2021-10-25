<div align="center">

# Backend
  
</div>

---

## How to run back-end
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

## Makefile info

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

## Account

| type                | username | password  | note                                               |
|---------------------|----------|-----------|----------------------------------------------------|
| admin site (Django) | admin    | 12345678  |                                                    |
| postgreSQL          | pl_user  | asd123!@# | host: localhost:5433 \| DB name: travel_management |