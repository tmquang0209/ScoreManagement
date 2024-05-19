import requests
from API.url import API_URL
from modules import localStorage

def getAllEmployees():
    url = API_URL + "/employee/all"
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    response = requests.get(url, headers=headers)
    return response.json()

def getEmployeeById(id):
    url = API_URL + "/employee/details/" + id
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    response = requests.get(url, headers=headers)
    return response.json()

def createEmployee(data):
    url = API_URL + "/employee/create"
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

def updateEmployee(id, data):
    url = API_URL + "/employee/update/" + str(id)
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    response = requests.put(url, headers=headers, json=data)
    return response.json()

def deleteEmployee(id):
    url = API_URL + "/employee/delete/" + str(id)
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    response = requests.delete(url, headers=headers)
    return response.json()