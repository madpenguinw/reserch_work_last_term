FROM node:21-alpine

WORKDIR /app

COPY package.json ./
COPY Processor.js ./

RUN npm install

COPY . .

ENV PORT=9000

EXPOSE $PORT

CMD ["node", "app.js"]
