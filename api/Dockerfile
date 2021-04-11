FROM node:15.14.0-alpine3.13

RUN apk --no-cache add --virtual builds-deps build-base python git

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY package.json /usr/src/app/

COPY . /usr/src/app/

RUN npm install 

EXPOSE 53385