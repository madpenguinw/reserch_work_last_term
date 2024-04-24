FROM node:21-alpine

WORKDIR /app

COPY package.json ./
COPY Processor.js ./

RUN npm install

COPY . .

# Определяем переменную окружения для порта
ENV PORT=9001

# Открываем порт для внешних запросов (используем значение переменной окружения)
EXPOSE $PORT

CMD ["node", "app.js"]