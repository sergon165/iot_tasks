FROM influxdb:1.8-alpine

WORKDIR /

ENV INFLUXDB_DB=data

EXPOSE 8086

VOLUME ["/var/lib/influxdb"]

CMD ["influxd"]