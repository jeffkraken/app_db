FROM alpine:latest

RUN apk add --no-cache sqlite

WORKDIR /data

COPY init.db /init.db
COPY sampledata.csv /sampledata.csv

CMD ["sh", "-c", "sqlite3 database.db < /init.db && tail -f /dev/null"]
