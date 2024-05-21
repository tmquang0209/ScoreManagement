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

    def handleOpenSemesters(self):
        self.controller.screens["Semester"].initData()
        self.controller.showFrame("Semester")

    def handleOpenSemesterCreate(self):
        # self.controller.screens["SemesterCreate"].initUI()
        self.controller.showFrame("SemesterCreate")

    def handleOpenSchedule(self):
        self.controller.screens["Schedule"].initData()
        self.controller.showFrame("Schedule")

    def handleOpenEnrollment(self):
        # self.controller.screens["Enrollment"].initData()
        self.controller.showFrame("Enrollment")

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

        department = personalInfo["department"]["name"] if "department" in personalInfo and personalInfo["department"] else None

        if roleName == "ADMIN" or department == "Phòng đào tạo":
            subjectMenu = Menu(menu, tearoff=0)
            subjectMenu.add_command(label="Danh sách môn học", command=self.handleOpenSubjects)
            subjectMenu.add_command(label="Thêm môn học mới", command=lambda: self.controller.showFrame("SubjectCreate"))
            menu.add_cascade(label="Môn học", menu=subjectMenu)

        if roleName == "ADMIN":
            departmentMenu = Menu(menu, tearoff=0)
            departmentMenu.add_command(label="Danh sách khoa/ phòng ban", command=self.handleOpenDepartments)
            departmentMenu.add_command(label="Thêm khoa/ phòng ban mới", command=lambda: self.controller.showFrame("DepartmentCreate"))
            menu.add_cascade(label="Quản lý khoa/ phòng ban", menu=departmentMenu)

            majorMenu = Menu(menu, tearoff=0)
            majorMenu.add_command(label="Danh sách ngành học", command=self.handleOpenMajors)
            majorMenu.add_command(label="Thêm ngành học mới", command=lambda: self.controller.showFrame("MajorCreate"))
            menu.add_cascade(label="Ngành học", menu=majorMenu)

            employeeMenu = Menu(menu, tearoff=0)
            employeeMenu.add_command(label="Danh sách nhân viên", command=self.handleOpenStaffs)
            employeeMenu.add_command(label="Thêm nhân viên mới", command=lambda: self.controller.showFrame("EmployeeCreate"))

            menu.add_cascade(label="Nhân viên", menu=employeeMenu)

            teacherMenu = Menu(menu, tearoff=0)
            teacherMenu.add_command(label="Danh sách giảng viên", command=self.handleOpenTeachers)
            teacherMenu.add_command(label="Thêm giảng viên mới", command=lambda: self.controller.showFrame("TeacherCreate"))
            menu.add_cascade(label="Giảng viên", menu=teacherMenu)

        if roleName == "ADMIN" or department == "Phòng đào tạo":
            studentMenu = Menu(menu, tearoff=0)
            studentMenu.add_command(label="Danh sách sinh viên", command=self.handleOpenStudents)
            studentMenu.add_command(label="Thêm sinh viên mới", command=lambda: self.controller.showFrame("StudentCreate"))
            menu.add_cascade(label="Sinh viên", menu=studentMenu)

            yearMenu = Menu(menu, tearoff=0)

            subYearMenu = Menu(yearMenu, tearoff=0)
            subYearMenu.add_command(label="Danh sách năm học", command=lambda: self.controller.showFrame("Years"))
            subYearMenu.add_command(label="Thêm năm học mới", command=lambda: self.controller.showFrame("YearCreate"))
            yearMenu.add_cascade(label="Năm học", menu=subYearMenu)

            subSemesterMenu = Menu(yearMenu, tearoff=0)
            subSemesterMenu.add_command(label="Danh sách học kỳ", command=self.handleOpenSemesters)
            subSemesterMenu.add_command(label="Thêm học kỳ mới", command=self.handleOpenSemesterCreate)
            yearMenu.add_cascade(label="Học kỳ", menu=subSemesterMenu)

            scheduleMenu = Menu(menu, tearoff=0)
            scheduleMenu.add_command(label="Danh sách lịch học", command=self.handleOpenSchedule)
            scheduleMenu.add_command(label="Thêm lịch học mới", command=lambda: self.controller.showFrame("ScheduleCreate"))
            yearMenu.add_cascade(label="Lịch học", menu=scheduleMenu)

            enrollmentMenu = Menu(menu, tearoff=0)
            enrollmentMenu.add_command(label="Danh sách đăng ký", command=self.handleOpenEnrollment)
            yearMenu.add_cascade(label="Đăng ký", menu=enrollmentMenu)

            menu.add_cascade(label="Năm học", menu=yearMenu)

        if roleName == "TEACHER" or roleName == "ADMIN" or department == "Phòng đào tạo":
            scoreMenu = Menu(menu, tearoff=0)
            scoreMenu.add_command(label="Nhập điểm", command=lambda: self.controller.showFrame("ScoreCreate"))
            scoreMenu.add_command(label="Danh sách điểm", command=lambda: self.controller.showFrame("Scores"))

        return menu

    def destroyMenu(self):
        self.controller.config(menu=None)
