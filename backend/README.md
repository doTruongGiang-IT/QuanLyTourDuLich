## How to run back-end
1. di chuyển đến thư mục `\QuanLyTourDuLich\backend\travel_management` 
2. Build docker image

```
docker build -t pl_backend .
```

hoặc

```
make build
```


3. Run server bằng docker-compose

```
docker-compose -p travel_management up
```

hoặc

```
make up
```

4. Khởi tạo Database

```
docker exec -it pl_backend pipenv run python3 manage.py migrate
```

hoặc

```
make init
```
