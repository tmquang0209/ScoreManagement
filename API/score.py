import requests
from API.url import API_URL
from modules import localStorage

def getScores(semesterId):
    url = API_URL + "/score"
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

def getByStudentIdAndScheduleId(scheduleId, studentId):
    url = API_URL + "/score/schedules/" + str(scheduleId) + "/" + str(studentId)
    token = localStorage.getItem("token")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    return response.json()

def getByScheduleId(scheduleId):
    url = API_URL + "/score/schedule/" + str(scheduleId)
    token = localStorage.getItem("token")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    return response.json()

def search(semesterId, subjectId, studentId = None):
    url = API_URL + "/score/search"
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

def update(scheduleId, data):
    url = API_URL + "/score/update/" + str(scheduleId)
    token = localStorage.getItem("token")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.put(url, headers=headers, json=data)

    return response.json()

def create(semesterId, subjectId, data):
    url = API_URL + "/score/create/" + str(semesterId) + "/" + str(subjectId)
    token = localStorage.getItem("token")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(url, headers=headers, json=data)

    return response.json()