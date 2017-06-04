FROM node:alpine
EXPOSE 3000

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apk update && apk upgrade && apk add --no-cache git && npm install -g bower

COPY src/package.json /usr/src/app/
COPY src/.bowerrc /usr/src/app/
COPY src/bower.json /usr/src/app/

RUN npm install
RUN bower install --allow-root

COPY src/* /usr/src/app/

CMD ["npm", "start"]
