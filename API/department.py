import requests

from API.url import API_URL

from modules import localStorage

def getDepartments():
    url = API_URL + "/department/all"
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    return response.json()

def updateDepartment(id, data):
    url = API_URL + f"/department/update/{id}"
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.put(url, headers=headers, json=data)
    print(response.json())
    return response.json()

def createDepartment(data):
    url = API_URL + "/department/create"
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

def deleteDepartment(id):
    url = API_URL + f"/department/delete/{id}"
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.delete(url, headers=headers)
    return response.json()
