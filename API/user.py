import requests
from .url import API_URL
import json
import sqlite3
import modules.localStorage as localStorage

def verifyToken(token):
    url = API_URL + '/user/verifyToken'
    headers = {
        'Authorization': 'Bearer ' + token
    }
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    return data

def getPersonalInfo(token):
    url = API_URL + '/user/info'
    headers = {
        'Authorization': 'Bearer ' + token
    }
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    return data


def userLogin(username, password):
    url = API_URL + '/user/signin'
    payload = json.dumps({
                "username": username,
                "password": password
            })
    headers = {'Content-Type': 'application/json'}

    response = requests.request("POST", url, headers=headers, data=payload)
    loginData = response.json()
    if "data" in loginData and len(loginData["data"]) > 0:
        if('token' in loginData["data"][0]):
            token = loginData['data'][0]['token']
            localStorage.setItem("token", token)

            infoResponse = getPersonalInfo(token)

            if infoResponse['success'] == True:
                if 'data' in infoResponse and len(infoResponse['data']) > 0:
                    data = infoResponse['data'][0]
                    localStorage.setItem("user", json.dumps(data))

    return loginData


def updateInfo(id, data):
    url = API_URL + '/user/update/' + str(id)
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }
    response = requests.put(url, json=data, headers=headers)
    return response.json()

def changePassword(id, data):
    url = API_URL + '/user/changePassword/' + str(id)
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }
    response = requests.put(url, json=data, headers=headers)
    return response.json()