import requests
from modules import localStorage

from API.url import API_URL

def getAllSemesters():
    url = f"{API_URL}/semester/all"
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    semesters = response.json()
    return semesters

def getSemesterByYear(id):
    url = f"{API_URL}/semester/year/{id}"
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    semester = response.json()
    return semester

def createSemester(data):
    url = f"{API_URL}/semester/create"
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

def updateSemester(id, data):
    url = f"{API_URL}/semester/update/{id}"
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.put(url, headers=headers, json=data)
    return response.json()


def deleteSemester(id):
    url = f"{API_URL}/semester/delete/{id}"
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.delete(url, headers=headers)
    return response.json()
