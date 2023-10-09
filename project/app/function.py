import numpy as np
import pandas as pd
from scipy import stats, interpolate
from influxdb import InfluxDBClient

influx_host = 'influx'
influx_port = 8086
influx_db = 'data'


def process_data(file, datetime_col, data_col, measurement, interval):
    data = pd.read_csv(file)
    data = data.dropna(subset=[data.columns[data_col]])
    data.iloc[:, datetime_col] = pd.to_datetime(data.iloc[:, datetime_col], format='%d.%m.%Y %H:%M')

    # Подключение к БД
    client = InfluxDBClient(host=influx_host, port=influx_port)
    client.switch_database(influx_db)

    # Запись исходных данных
    for index, row in data.iterrows():
        json_body = [
            {
                "measurement": f"{measurement}_raw",
                "time": row.iloc[datetime_col],
                "fields": {
                    "value": row.iloc[data_col],
                }
            }
        ]
        client.write_points(json_body)

    # Интерполяция
    min_date = data.iloc[:, datetime_col].min()
    max_date = data.iloc[:, datetime_col].max()

    data['seconds'] = data.iloc[:, datetime_col].apply(lambda x: x - min_date)
    x = data['seconds'].astype(int) // 10 ** 9
    y = data.iloc[:, data_col]

    f = interpolate.interp1d(x, y)
    end = int((max_date - min_date).total_seconds())
    x1 = np.arange(0, end, interval)
    y1 = f(x1)

    # Запись полученных данных
    for i in range(len(x1)):
        json_body = [
            {
                "measurement": f"{measurement}_new",
                "time": min_date + pd.Timedelta(seconds=x1[i]),
                "fields": {
                    "value": y1[i],
                }
            }
        ]
        client.write_points(json_body)

    client.close()


if __name__ == '__main__':
    with open('../data/weather.csv') as file:
        process_data(file, 0, 1, 'test', 3600)
