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

        roleName = personalInfo["role"]["name"] if "role" in personalInfo else None

        if roleName == "ADMIN":
            subjectMenu = Menu(menu, tearoff=0)
            subjectMenu.add_command(label="Danh sách môn học", command=self.handleOpenSubjects)
            subjectMenu.add_command(label="Thêm môn học mới", command=lambda: self.controller.showFrame("SubjectCreate"))
            menu.add_cascade(label="Môn học", menu=subjectMenu)

            departmentMenu = Menu(menu, tearoff=0)
            departmentMenu.add_command(label="Danh sách khoa/ phòng ban", command=self.handleOpenDepartments)
            departmentMenu.add_command(label="Thêm khoa/ phòng ban mới", command=lambda: self.controller.showFrame("DepartmentCreate"))
            menu.add_cascade(label="Quản lý khoa/ phòng ban", menu=departmentMenu)

            majorMenu = Menu(menu, tearoff=0)
            majorMenu.add_command(label="Danh sách ngành học", command=self.handleOpenMajors)
            majorMenu.add_command(label="Thêm ngành học mới", command=lambda: self.controller.showFrame("MajorCreate"))
            menu.add_cascade(label="Ngành học", menu=majorMenu)

            teacherMenu = Menu(menu, tearoff=0)
            teacherMenu.add_command(label="Danh sách giảng viên")
            teacherMenu.add_command(label="Thêm giảng viên mới")
            menu.add_cascade(label="Giảng viên", menu=teacherMenu)

            studentMenu = Menu(menu, tearoff=0)
            studentMenu.add_command(label="Danh sách sinh viên")
            studentMenu.add_command(label="Thêm sinh viên mới")
            menu.add_cascade(label="Sinh viên", menu=studentMenu)

            semesterMenu = Menu(menu, tearoff=0)

            subMenu = Menu(semesterMenu, tearoff=0)
            subMenu.add_command(label="Danh sách năm học", command=lambda: self.controller.showFrame("Years"))
            subMenu.add_command(label="Thêm năm học mới", command=lambda: self.controller.showFrame("YearCreate"))
            semesterMenu.add_cascade(label="Năm học", menu=subMenu)

            subMenu1 = Menu(semesterMenu, tearoff=0)
            subMenu1.add_command(label="Danh sách học kỳ")
            subMenu1.add_command(label="Thêm học kỳ mới")
            semesterMenu.add_cascade(label="Học kỳ", menu=subMenu1)

            menu.add_cascade(label="Năm học", menu=semesterMenu)

        elif roleName == "MANAGER":
            managerMenu = Menu(menu, tearoff=0)
            managerMenu.add_command(label="Quản lý điểm")
            menu.add_cascade(label="Manager", menu=managerMenu)

        return menu

    def destroyMenu(self):
        self.controller.config(menu=None)
