import requests

from API.url import API_URL
from modules import localStorage

def getAllTeachers():
    url = API_URL + "/teacher/all"
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    return response.json()

def getTeacherById(teacherId):
    url = API_URL + f"/teacher/details/{str(teacherId)}"
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    return response.json()


def createTeacher(data):
    url = API_URL + "/teacher/create"
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

def updateTeacher(id, data):
    url = API_URL + f"/teacher/update/{str(id)}"
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.put(url, headers=headers, json=data)
    return response.json()

def deleteTeacher(id):
    url = API_URL + f"/teacher/delete/{str(id)}"
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.delete(url, headers=headers)
    return response.json()
