import requests
from API.url import API_URL

def getAllYears():
    url = API_URL + "/year/all"
    response = requests.get(url)
    return response.json()
