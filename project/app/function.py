import numpy as np
import pandas as pd
from scipy import stats, interpolate
from influxdb import InfluxDBClient

influx_host = 'localhost'
influx_port = 8086
influx_db = 'data'

interval = 3600

data = pd.read_csv('../data/weather.csv')
data = data.dropna(subset=[data.columns[1]])
data.iloc[:, 0] = pd.to_datetime(data.iloc[:, 0], format='%d.%m.%Y %H:%M')

# Подключение к БД
client = InfluxDBClient(host=influx_host, port=influx_port)
client.switch_database(influx_db)

# Запись исходных данных
for index, row in data.iterrows():
    json_body = [
        {
            "measurement": "raw_data",
            "time": row.iloc[0],
            "fields": {
                "value": row.iloc[1],
            }
        }
    ]
    client.write_points(json_body)

# Интерполяция
min_date = data.iloc[:, 0].min()
max_date = data.iloc[:, 0].max()

x = (data.iloc[:, 0] - min_date).astype(int) // 10**9
y = data.iloc[:, 1]

f = interpolate.interp1d(x, y)
end = int((max_date - min_date).total_seconds())
x1 = np.arange(0, end, interval)
y1 = f(x1)

# Запись полученных данных
for i in range(len(x1)):
    json_body = [
        {
            "measurement": "new_data",
            "time": min_date + pd.Timedelta(seconds=x1[i]),
            "fields": {
                "value": y1[i],
            }
        }
    ]
    client.write_points(json_body)
