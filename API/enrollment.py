import requests

from API.url import API_URL

from modules import localStorage

def getEnrollments(scheduleId):
    url = API_URL + "/enrollment/search"
    token = localStorage.getItem("token")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    data = {
        "scheduleId": scheduleId
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

def addEnrollment(scheduleId, studentId):
    url = API_URL + "/enrollment/add"
    token = localStorage.getItem("token")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    data = {
        "scheduleId": scheduleId,
        "studentId": studentId,
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

def deleteEnrollment(studentId, scheduleId):
    url = API_URL + "/enrollment/delete/" + str(scheduleId) + "/" + str(studentId)
    token = localStorage.getItem("token")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.delete(url, headers=headers)

    return response.json()