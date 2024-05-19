import requests

from modules import localStorage

from API.url import API_URL

def getAllRoles():
    url = API_URL + "/role/all"
    token = localStorage.getItem("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    response = requests.get(url, headers=headers)
    return response.json()