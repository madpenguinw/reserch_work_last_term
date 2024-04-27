FROM node:21-alpine

WORKDIR /usr/src/app

COPY package.json .
COPY yarn.lock .

RUN yarn
COPY . .
RUN yarn build

EXPOSE 3000

ENTRYPOINT yarn run preview

