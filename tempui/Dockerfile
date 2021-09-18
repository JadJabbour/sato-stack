FROM node:12-alpine

RUN apk --no-cache add --virtual builds-deps build-base python git

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY package.json /usr/src/app/

COPY . /usr/src/app/

RUN npm install  && \
    npm rebuild node-sass --build-from-source

EXPOSE 80 80