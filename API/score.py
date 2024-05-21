import requests
from API.url import API_URL
from modules import localStorage

def getScores(semesterId):
    url = API_URL + "/scores"
    token = localStorage.getItem("token")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    data = {
        "semesterIds": semesterId
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

def getByStudentId(studentId):
    url = API_URL + "/scores/student/" + studentId
    token = localStorage.getItem("token")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    return response.json()

def search(semesterId, subjectId, studentId = None):
    url = API_URL + "/scores/search"
    token = localStorage.getItem("token")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    data = {
        "semesterId": semesterId,
        "subjectId": subjectId,
        "studentId": studentId
    }

    response = requests.post(url, headers=headers, json=data)

    return response.json()

def update(scoreId, midTerm = None, final = None):
    url = API_URL + "/scores"
    token = localStorage.getItem("token")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    data = {
        "scoreId": scoreId,
        "midTerm": midTerm,
        "final": final
    }

    response = requests.put(url, headers=headers, json=data)

    return response.json()