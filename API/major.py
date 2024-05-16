import requests
import json

from modules import localStorage
from API.url import API_URL

def getAllMajors():
    url = API_URL + "/major/all"
    response = requests.get(url)

    return response.json()

def getMajorById(id):
    url = API_URL + "/major/details/" + str(id)
    response = requests.get(url)

    return response.json()

def createMajor(data):
    url = API_URL + "/major/create"
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

def updateMajor(id, data):
    url = API_URL + f"/major/update/{str(id)}"
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.put(url, headers=headers, json=data)
    return response.json()

def deleteMajor(id):
    url = API_URL + "/major/delete/" + str(id)
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    response = requests.delete(url, headers=headers)

    return response.json()
