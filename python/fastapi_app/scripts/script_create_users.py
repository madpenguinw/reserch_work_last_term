import json
import random
import string


def random_string(length=10):
    """Generate a random string of fixed length"""
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))


def random_age():
    """Generate a random age between 18 and 70"""
    return random.randint(18, 70)


def generate_user():
    """Generate a single user dictionary"""
    return {
        "firstname": random_string(7).capitalize(),
        "lastname": random_string(10).capitalize(),
        "patronymic": random_string(10).capitalize(),
        "age": random_age(),
    }


def generate_users(count=10000):
    """Generate a list of user dictionaries"""
    return [generate_user() for _ in range(count)]


if __name__ == "__main__":
    users = generate_users(10000)
    with open("data.json", "w") as f:
        json.dump(users, f, indent=4)

    print("Generated data.json with 10,000 unique users.")
