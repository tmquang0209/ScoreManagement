from localStoragePy import localStoragePy
localStorage = localStoragePy('ScoreApp', 'sqlite')

def setItem(key, value):
    localStorage.setItem(key, value)

def getItem(key):
    return localStorage.getItem(key)

def removeItem(key):
    return localStorage.removeItem(key)

def clear():
    return localStorage.clear()