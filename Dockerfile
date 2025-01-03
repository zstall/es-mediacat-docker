# FROM python:3.12-alpine

# RUN apk add --no-cache --virtual .build-deps \
#     gcc \
#     python3-dev \
#     musl-dev \
#     postgresql-dev \
#     && pip install --no-cache-dir psycopg2 \
#     && apk del --no-cache .build-deps

# RUN apk add mediainfo

# WORKDIR /mediacatapp
# COPY . /mediacatapp
# RUN pip install -r requirements.txt
# EXPOSE 5000
# CMD ["flask", "--app", "main", "run", "-h", "0.0.0.0", "-p", "5000"]

FROM python:3.12.6
WORKDIR /mediacatapp
COPY . /mediacatapp
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install -y mediainfo
RUN apt-get clean
EXPOSE 5000
CMD flask --app main run -h 0.0.0.0 -p 5000

# Find lighter testing files to bring down repo size