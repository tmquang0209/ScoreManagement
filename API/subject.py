import requests

from API.url import API_URL
from modules import localStorage

def getAllSubjects():
    url = API_URL + "/subject/all"
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    return response.json()

def search(keyword):
    url = API_URL + "/subject/search/" + keyword
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    return response.json()


def getSubjectById(subjectId):
    url = API_URL + f"/subject/details/{str(subjectId)}"
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    return response.json()

def createSubject(data):
    url = API_URL + "/subject/create"
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

def updateSubject(id, data):
    url = API_URL + f"/subject/update/{str(id)}"
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.put(url, headers=headers, json=data)
    return response.json()

def deleteSubject(id):
    url = API_URL + f"/subject/delete/{str(id)}"
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.delete(url, headers=headers)
    return response.json()