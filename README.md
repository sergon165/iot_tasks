# Задание 1
1. **Docker** и **Docker Desktop** уже были установлены на компьютере.
2. Учетная запись на **Dockerhub** уже имеется (*sergon165*).
3. Выполнена загрузка docker-образа **python:3.12-alpine**.
```commandline
docker pull python:3.12-alpine
```

4. Создан минимальный проект на Python из 1 файла (*main.py*).

*main.py*:
```python
print('Hello, Docker!')
```

5. Создан *Dockerfile*, который копирует *main.py* в контейнер и запускает его.

*Dockerfile*:
```dockerfile
FROM python:3.12-alpine
COPY main.py /
CMD ["python3", "./main.py"]
```

6. Проект упакован в docker-образ.
```commandline
docker build -t sergon165/iot-task1
```

7. Docker-образ запущен.
```commandline
docker run sergon165/iot-task1
```
Результат:
![Запуск образа](img/task1-run.png)

8. Проект выгружен на Dockerhub.
```commandline
docker push sergon165/iot-task1
```

# Задание 2
## Создание *Dockerfile* для InfluxDB
1. Использован docker-образ influxdb:1.8-alpine.
   
```dockerfile
FROM influxdb:1.8-alpine 
```

2. Указана рабочая директория.
```dockerfile
WORKDIR /
```

3. Указана переменная окружения для создания базы данных.
```dockerfile
ENV INFLUXDB_DB=data
```

4. Указан порт 8086.
```dockerfile
EXPOSE 8086
```

5. Задана команда, которая выполняется при старте контейнера.
```dockerfile
CMD ["influxd"]
```

## Сборка и запуск
1. Произведена сборка образа.
```commandline
docker build -t iot-influx .
```

2. Произведен запуск образа с открытием порта.
```commandline
docker run -p 8086:8086 iot-influx
```

## Проверка
1. В проект добавлен *weather.csv* (данные о температуре в Перми за сентябрь).
2. В проект добавлен *function.py*, который:
    1. считывает данные из *weather.csv*,
    2. записывает их в InfluxDB (measurement "raw_data"),
    3. делает интерполяцию с интервалом в 1 час,
    4. записывает полученные данные в InfluxDB (measurement "new_data").
    
3. Запущен *function.py*.

raw_data:
![raw_data](img/task2-raw_data.png)

new_data:
![new_data](img/task2-new_data.png)


Из графиков видно, что программе успешно получилось подключиться к InfluxDB и записать данные.