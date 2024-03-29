
# pull official base image
FROM python:3.8.3-alpine

RUN apk update && apk add gcc libxml2-dev libxslt-dev python3-dev musl-dev jpeg-dev zlib-dev libffi-dev openssl-dev make

# set work directory
WORKDIR /usr/src/encryptor

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip3 install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup -S app && adduser -S app -G app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
WORKDIR $APP_HOME


# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app