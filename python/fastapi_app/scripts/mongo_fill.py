import json

from pymongo import MongoClient

# Подключение к MongoDB
client = MongoClient(
    "localhost",
    3456,
    username="admin",
    password="12345678",
    authSource="admin",
)
db = client["VKR"]
collection = db["users"]

# Чтение данных из файла data.json и добавление их в коллекцию
with open("data.json", "r") as file:
    data = json.load(file)
    collection.insert_many(data)

# Закрытие соединения с MongoDB
client.close()
