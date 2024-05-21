FROM node:21-alpine

WORKDIR /app

COPY . .

RUN npm install

ENV PORT=9002

EXPOSE $PORT

CMD ["node", "app.js"]
