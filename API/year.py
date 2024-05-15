import requests
from modules import localStorage

from API.url import API_URL

def getAllYears():
    url = API_URL + "/year/all"
    response = requests.get(url)
    return response.json()

def createYear(year, tuition):
    url = API_URL + "/year/create"
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    payload = {
        "year": year,
        "tuition": tuition
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def deleteYear(yearId):
    url = API_URL + "/year/delete/" + str(yearId)
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    response = requests.delete(url, headers=headers)
    return response.json()

def getYearById(yearId):
    url = API_URL + "/year/" + str(yearId)
    response = requests.get(url)
    return response.json()

def updateYear(yearId, yearInput, tuitionInput):
    url = API_URL + "/year/update/" + str(yearId)
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    payload = {
        "year": yearInput,
        "tuition": tuitionInput
    }

    response = requests.put(url, json=payload, headers=headers)
    return response.json()