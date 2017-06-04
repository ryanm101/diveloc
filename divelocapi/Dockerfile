FROM node:alpine
EXPOSE 3000

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY src/package.json /usr/src/app/
RUN npm install

COPY src/* /usr/src/app/

CMD ["npm", "start"]
