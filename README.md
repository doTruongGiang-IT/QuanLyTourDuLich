<div align="center">

# Travel Management

<img src="/readme/banner.png" width="56%">

![VERSION: V0.2.0 (shields.io)](https://img.shields.io/badge/version-v0.2.0-1ED760?&style=for-the-badge&logo=qgis&logoColor=white)
![DJANGO (shields.io)](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![REACT (shields.io)](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![DEAR PYGUI (shields.io)](https://img.shields.io/badge/Dear%20Pygui-00AEED?style=for-the-badge&logo=PlayCanvas&logoColor=FFD519)
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
Travel Management là hệ thống quản lý tour du lịch đơn giản và dễ dàng. Hệ thống được triển khai trên nền tảng web app và desktop app.

### Các tính năng của hệ thống

Hệ thống quản lý tất cả thông tin liên quan:
+ Quản lý tour
+ Quản lý đoàn khách

và thực hiện các yêu cầu quản lý, ví dụ:
+ Lập danh sách các khách hàng của một đoàn du lịch nào đó
+ Lập danh sách các địa điểm của một tour nào đó.
+ Thống kê chi phí (một tour, chi phí khách sạn, ăn uống trong một khoảng thời gian…).
+ Doanh thu của một đoàn, của một tour trong một khoảng thời gian.
+ Tìm kiếm thông tin về một khách hàng, về một đoàn, về một tour.
+ Xem bảng giá tour hiện tại
+ Thống kê tình hình hoạt động theo mỗi tour (doanh số, số đoàn tham quan,…)
+ Thống kê số lần đi tour của từng nhân viên trong khoảng thời gian.

### System architecture

<div align="center">
<img src="/readme/system-architecture.png" width="77%">
</div>

<br>

## Front-end
Front-end using **React**.

### How to run front-end
**1. Di chuyển đến thư mục** `\QuanLyTourDuLich\frontend`

**2. Build docker image**

```shell
docker build -t pl_frontend .
```

*hoặc*

```shell
make build
```

**3. Run server bằng docker-compose**

```shell
docker-compose -p travel_management_fe up
```

*hoặc*

```shell
make up
```

### Makefile info

| rule    | command                                                                 | description                        | note                             |
|---------|-------------------------------------------------------------------------|------------------------------------|----------------------------------|
| build   | docker build -t pl_frontend .                                           | build image for front-end          |                                  |
| up      | docker-compose -p travel_management_fe up                               | start app                          |                                  |
| down    | docker-compose -p travel_management_fe down                             | down compose                       |                                  |
| restart | docker-compose -p travel_management_fe down                             | restart compose                    |                                  |
|         | docker-compose -p travel_management_fe up                               |                                    |                                  |

<br>

## Back-end

Back-end using **Django** for building REST API.

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


### Account

| type                | username | password  | note                                               |
|---------------------|----------|-----------|----------------------------------------------------|
| admin site (Django) | admin    | 12345678  |                                                    |
| postgreSQL          | pl_user  | asd123!@# | host: localhost:5433 \| DB name: travel_management |

> Các environment variable được định nghĩa ở dev.env

<br>

## Desktop app
Desktop app using **Dear PyGui**.

<br>

## Document
Document [here](https://github.com/doTruongGiang-IT/QuanLyTourDuLich/tree/develop/document) 
and API document [here](https://github.com/doTruongGiang-IT/QuanLyTourDuLich/wiki/API-Document-v1)

<br>

## Try it now
Easy and quick to deploy with

*Main branch*\
[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/doTruongGiang-IT/QuanLyTourDuLich)

*Develop branch*\
[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/doTruongGiang-IT/QuanLyTourDuLich/tree/develop)

