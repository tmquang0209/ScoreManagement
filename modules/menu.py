import json
from tkinter import *
from tkinter.ttk import *
import modules.localStorage as localStorage

class MenuManager:
    def __init__(self, controller):
        self.controller = controller
        self.localStorage = localStorage

    def logout(self):
        self.controller.screens["PersonalInfo"].clearPersonalInfo()
        self.localStorage.clear()
        self.controller.config(menu=None)
        self.controller.showFrame("Login")

    def handleOpenPersonalInfo(self):
        self.controller.screens["PersonalInfo"].preparePersonalInfo()
        self.controller.showFrame("PersonalInfo")

    def handleOpenSubjects(self):
        self.controller.screens["Subjects"].initData()
        self.controller.showFrame("Subjects")

    def handleOpenDepartments(self):
        self.controller.screens["Department"].initData()
        self.controller.showFrame("Department")

    def handleOpenMajors(self):
        self.controller.screens["Major"].initData()
        self.controller.showFrame("Major")

    def handleOpenStaffs(self):
        self.controller.screens["Employee"].initData()
        self.controller.showFrame("Employee")

    def handleOpenTeachers(self):
        self.controller.screens["Teacher"].initData()
        self.controller.showFrame("Teacher")

    def handleOpenStudents(self):
        self.controller.screens["Student"].initData()
        self.controller.showFrame("Student")

    def handleOpenYears(self):
        self.controller.screens["Years"].initData()
        self.controller.showFrame("Years")

    def handleOpenSchedule(self):
        self.controller.screens["Schedule"].initData()
        self.controller.showFrame("Schedule")

    def handleOpenEnrollment(self):
        self.controller.screens["Enrollment"].initData()
        self.controller.showFrame("Enrollment")

    def handleOpenScore(self):
        self.controller.screens["Score"].initData()
        self.controller.showFrame("Score")

    def createMenu(self):
        personalInfo = self.localStorage.getItem("user")
        personalInfo = json.loads(personalInfo) if personalInfo else {}

        menu = Menu(self.controller)
        accountMenu = Menu(menu, tearoff=0)
        accountMenu.add_command(label="Thông tin cá nhân", command=self.handleOpenPersonalInfo)
        accountMenu.add_command(label="Đổi mật khẩu", command=lambda: self.controller.showFrame("ChangePassword"))
        accountMenu.add_separator()
        accountMenu.add_command(label="Đăng xuất", command=self.logout)
        menu.add_cascade(label="Tài khoản", menu=accountMenu)

        roleName = personalInfo["role"]["name"] if "role" in personalInfo and "name" in personalInfo["role"] else None

        department = personalInfo["department"]["name"] if "department" in personalInfo and personalInfo["department"] else None


        if roleName == "ADMIN" or department == "Phòng đào tạo" or "teacherCode" in personalInfo or roleName == "TEACHER":
            educationMenu = Menu(menu, tearoff=0)
            if roleName == "ADMIN" or department == "Phòng đào tạo":
                educationMenu.add_command(label="Năm học", command=self.handleOpenYears)
                educationMenu.add_command(label="Môn học", command=self.handleOpenSubjects)
                educationMenu.add_command(label="Ngành học", command=self.handleOpenMajors)
            educationMenu.add_command(label="Lịch học", command=self.handleOpenSchedule)
            educationMenu.add_command(label="Đăng ký học", command=self.handleOpenEnrollment)
            # educationMenu.add_command(label="Điểm", command=self.handleOpenScore)
            menu.add_cascade(label="Đào tạo", menu=educationMenu)

        if roleName == "ADMIN":
            userMenu = Menu(menu, tearoff=0)
            userMenu.add_command(label="Nhân viên", command=self.handleOpenStaffs)
            userMenu.add_command(label="Giảng viên", command=self.handleOpenTeachers)
            userMenu.add_command(label="Sinh viên", command=self.handleOpenStudents)
            menu.add_cascade(label="Người dùng", menu=userMenu)

            departmentMenu = Menu(menu, tearoff=0)
            departmentMenu.add_command(label="Khoa/ Phòng ban", command=self.handleOpenDepartments)
            menu.add_cascade(label="Khoa/ Phòng ban", menu=departmentMenu)
        return menu

    def destroyMenu(self):
        self.controller.config(menu=None)
