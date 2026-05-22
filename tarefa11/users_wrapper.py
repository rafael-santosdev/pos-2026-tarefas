import requests

API_URL = "https://jsonplaceholder.typicode.com"


def list():
    response = requests.get(f"{API_URL}/users")
    if response.status_code == 200:
        return response.json()

    return False


def create(user_data):
    response = requests.post(f"{API_URL}/users", json=user_data)
    if response.status_code == 201:
        return response.json()

    return False


def read(user_id):
    response = requests.get(f"{API_URL}/users/{user_id}")
    if response.status_code == 200:
        return response.json()

    return False


def update(user_id, user_data):
    response = requests.put(f"{API_URL}/users/{user_id}", json=user_data)
    if response.status_code == 200:
        return response.json()

    return False


def delete(user_id):
    response = requests.delete(f"{API_URL}/users/{user_id}")
    if response.status_code == 204:
        return True

    return False


def todos(user_id):
    response = requests.get(f"{API_URL}/users/{user_id}/todos") 
    if response.status_code == 200:
        return response.json()

    return False