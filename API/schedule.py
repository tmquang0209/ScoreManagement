import requests
from modules import localStorage

from API.url import API_URL

def getAllSchedules():
    url = API_URL + "/schedule/all"
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    response = requests.get(url, headers=headers)
    return response.json()

def getScheduleById(id):
    url = API_URL + "/schedule/details/" + id
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    response = requests.get(url, headers=headers)
    return response.json()

def createSchedule(data):
    url = API_URL + "/schedule/create"
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

def updateSchedule(id, data):
    url = API_URL + "/schedule/update/" + str(id)
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    response = requests.put(url, headers=headers, json=data)
    return response.json()

def deleteSchedule(id):
    url = API_URL + "/schedule/delete/" + str(id)
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    response = requests.delete(url, headers=headers)
    return response.json()