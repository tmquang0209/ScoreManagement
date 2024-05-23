from tkinter import *
from tkinter.ttk import *

import json

from screens.home import Home
from screens.login import Login
from screens.years import Years
from screens.YearAction.create import YearCreate
from screens.personalInfo import PersonalInfo
from screens.changePassword import ChangePassword
from screens.subjects import Subjects, SubjectCreate
from screens.department import Department, DepartmentCreate
from screens.major import Major, MajorCreate
from screens.employee import Employee, EmployeeCreate
from screens.teacher import Teacher, TeacherCreate
from screens.student import Student, StudentCreate
from screens.semester import Semester, SemesterCreate
from screens.schedule import Schedule, ScheduleCreate
from screens.enrollment import Enrollment, EnrollmentRecords
from screens.score import Score, ScoreCreate, ScoreDetail

from API.user import verifyToken, getPersonalInfo

import modules.localStorage as localStorage

class ScoreApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Hệ thống quản lý đào tạo")

        self.localStorage = localStorage

        self.token = self.checkToken()

        # Initial screen
        self.currentScreen = self.getInitialScreen()

        # Initialize container for stacking screens
        self.container = Frame(self, width=800, height=500)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, minsize=500, weight=2)
        self.container.grid_columnconfigure(0, minsize=600, weight=2)

        self.screens = {}

        for F in (Home, Login, Years, YearCreate, PersonalInfo, ChangePassword, Subjects, SubjectCreate, Department, DepartmentCreate, Major, MajorCreate, Teacher, TeacherCreate, Student, StudentCreate, Semester, SemesterCreate, Schedule, ScheduleCreate, Employee, EmployeeCreate, Enrollment, EnrollmentRecords, Score, ScoreCreate, ScoreDetail):
            pageName = F.__name__

            # if __init__ method has scheduleId parameter
            if pageName == "EnrollmentRecords" or pageName == "ScoreCreate" or pageName == "ScoreDetail":
                frame = F(parent=self.container, controller=self, scheduleId=None)
            else:
                frame = F(parent=self.container, controller=self)
            self.screens[pageName] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # self.screens["PersonalInfo"].preparePersonalInfo()

        self.showFrame(self.currentScreen)
        self.displayMenu()

    def displayMenu(self):
        if self.token:
            from modules.menu import MenuManager
            menuManager = MenuManager(controller=self)
            menu = menuManager.createMenu()
            self.config(menu=menu)
        else:
            self.config(menu=None)

    def destroyMenu(self):
        self.config(menu=None)

    def checkToken(self):
        token = self.localStorage.getItem("token")

        if token:
            response = verifyToken(token)
            if response["success"]:
                infoResponse = getPersonalInfo(response["data"][0])
                localStorage.setItem("user", json.dumps(infoResponse["data"][0]))
                localStorage.setItem("token", response["data"][0])
                return token
            else:
                localStorage.clear()
                return None
        else:
            return None

    def getInitialScreen(self):
        if self.token != None:
            return "Home"
        else:
            return "Login"

    def showFrame(self, pageName, scheduleId = None):
        if pageName not in self.screens:
            if scheduleId:
                frame = globals()[pageName](parent=self.container, controller=self, scheduleId=scheduleId)
            else:
                frame = globals()[pageName](parent=self.container, controller=self)
            self.screens[pageName] = frame
            frame.grid(row=0, column=0, sticky="nsew")

            # if pageName == "PersonalInfo":
            #     frame.preparePersonalInfo()

        for frame in self.screens.values():
            frame.tkraise()

        self.screens[pageName].tkraise()

# Run the application
if __name__ == "__main__":
    app = ScoreApp()
    app.mainloop()
