import requests

from API.url import API_URL
from modules import localStorage

def getAllStudents():
    url = API_URL + '/student/all'
    token = localStorage.getItem("token")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    return response.json()

def getStudentById(id):
    url = API_URL + f'/student/details/{id}'
    token = localStorage.getItem("token")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    return response.json()

def createStudent(data):
    url = API_URL + '/student/create'
    token = localStorage.getItem("token")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

def updateStudent(id, data):
    url = API_URL + f'/student/update/{id}'
    token = localStorage.getItem("token")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.put(url, headers=headers, json=data)
    return response.json()

def deleteStudent(id):
    url = API_URL + f'/student/delete/{id}'
    token = localStorage.getItem("token")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.delete(url, headers=headers)
    return response.json()