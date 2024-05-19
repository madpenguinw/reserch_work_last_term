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

# Получение списка коллекций
collections_list = db.list_collection_names()

# Вывод списка коллекций
print("Collections in VKR database:")
for collection_name in collections_list:
    print(collection_name)

# Закрытие соединения с MongoDB
client.close()
