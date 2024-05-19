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

# Получение первых 10 объектов из коллекции и вывод их в консоль
cursor = collection.find().limit(10)
for document in cursor:
    print(document)

# Закрытие соединения с MongoDB
client.close()
