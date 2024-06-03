from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

from API import enrollment as enrollmentAPI, year as yearAPI, semester as semesterAPI, subject as subjectAPI, schedule as scheduleAPI, student as studentAPI

class Enrollment(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.initUI()

    def handleYearChange(self, event, yearsList = []):
        year = yearsList[self.year.current()]["id"]

        self.semesters = semesterAPI.getSemesterByYear(year)["data"] if "data" in semesterAPI.getSemesterByYear(year) else []

        self.semester.set("")
        self.semester["values"] = [semester["semester"] for semester in self.semesters]

    def initUI(self):
        self.form = Frame(self)
        self.form.pack(pady=20)

        self.years = yearAPI.getAllYears()["data"] if "data" in yearAPI.getAllYears() else []
        self.semesters = []
        self.subjects = subjectAPI.getAllSubjects()["data"] if "data" in subjectAPI.getAllSubjects() else []

        Label(self.form, text="Năm học").grid(row=0, column=0)
        self.year = Combobox(self.form, values=[year["year"]for year in self.years])
        self.year.grid(row=0, column=1)
        self.year.bind("<<ComboboxSelected>>", lambda event:self.handleYearChange(event,yearsList=self.years))

        Label(self.form, text="Học kỳ").grid(row=0, column=2)
        self.semester = Combobox(self.form)
        self.semester.grid(row=0, column=3)

        Label(self.form, text="Môn học").grid(row=0, column=4)
        self.subject = Combobox(self.form, values=[subject["subjectName"] for subject in self.subjects])
        self.subject.grid(row=0, column=5)


        Label(self.form, text="Lớp").grid(row=0, column=6)
        self.className = Entry(self.form)
        self.className.grid(row=0, column=7)

        Button(self.form, text="Tìm kiếm", command=lambda: self.handleSearch(self.semesters, self.subjects)).grid(row=0, column=8)

        self.tree = Treeview(self, columns=("#1", "#2"), show="headings")
        self.tree.pack(pady=20)

        self.tree.column("#1", anchor=CENTER)
        self.tree.heading("#1", text="Lớp")

        self.tree.column("#2", anchor=CENTER)
        self.tree.heading("#2", text="Số lượng sinh viên")

        self.tree.bind("<Double-1>", self.viewRecords)
        # self.tree.bind("<Delete>", self.deleteEnrollment)

    def initData(self):
        print("init data")
        # years = yearAPI.getAllYears()["data"] if "data" in yearAPI.getAllYears() else []

        # subjects = subjectAPI.getAllSubjects()["data"] if "data" in subjectAPI.getAllSubjects() else []

        # self.updateForm(years, subjects)

    def updateForm(self, years = [], subjects = []):
        # add values to combobox
        self.year["values"] = [year["year"] for year in years]

    def updateData(self, data):
        self.tree.delete(*self.tree.get_children())

        for schedule in data:
            self.tree.insert("", "end", text=schedule["id"], values=(schedule["className"], schedule["currentStudent"]))

    def viewRecords(self, event):
        item = self.tree.selection()[0]
        scheduleId = self.tree.item(item, "text")
        self.controller.screens["EnrollmentRecords"].initData(scheduleId)
        self.controller.showFrame("EnrollmentRecords", scheduleId=scheduleId)

    def handleSearch(self, semesters = [], subjects = []):
        semesterId = semesters[self.semester.current()]["id"]

        subjectId = subjects[self.subject.current()]["id"] if self.subject.current() != -1 else None
        className = self.className.get()

        schedules = scheduleAPI.searchSchedules({
            "semesterId": semesterId,
            "subjectId": subjectId,
            "className": className if className != "" else None
        })["data"] if "data" in scheduleAPI.searchSchedules({
            "semesterId": semesterId,
            "subjectId": subjectId,
            "className": className if className != "" else None
        }) else []

        self.updateData(schedules)

    # def deleteEnrollment(self, event):
    #     item = self.tree.selection()[0]
    #     className = self.tree.item(item, "values")[0]
    #     if messagebox.askyesno("Xác nhận", f"Xác nhận xóa lớp {className}"):
    #         enrollmentAPI.deleteEnrollment(className)
    #         self.handleSearch()

class EnrollmentRecords(Frame):
    def __init__(self, parent, controller, scheduleId):
        Frame.__init__(self, parent)
        self.controller = controller
        self.scheduleId = scheduleId
        self.initUI()

    def initUI(self):
        self.form = Frame(self)
        self.form.pack(pady=20)

        Label(self.form, text="Sinh viên").grid(row=0, column=0, padx=5, pady=5)
        self.student = Combobox(self.form)
        self.student.grid(row=0, column=1, padx=5, pady=5)

        Button(self.form, text="Thêm", command=self.handleAdd).grid(row=0, column=2, padx=5, pady=5)

        self.tree = Treeview(self, columns=("#1", "#2"), show="headings")
        self.tree.pack(pady=20)

        self.tree.column("#1", anchor=CENTER)
        self.tree.heading("#1", text="Mã sinh viên")

        self.tree.column("#2", anchor=CENTER)
        self.tree.heading("#2", text="Họ tên")

        self.tree.bind("<Delete>", self.deleteRecord)

    def initData(self, scheduleId):
        self.scheduleId = scheduleId
        studentsList = studentAPI.getAllStudents()["data"] if "data" in studentAPI.getAllStudents() else []
        self.student["values"] = [student["studentCode"] for student in studentsList]

        self.students = enrollmentAPI.getEnrollments(scheduleId)["data"] if "data" in enrollmentAPI.getEnrollments(scheduleId) else []
        self.updateData()

    def updateData(self):
        self.tree.delete(*self.tree.get_children())

        # delete all items in tree
        for i in self.tree.get_children():
            self.tree.delete(i)

        for student in self.students:
            self.tree.insert("", "end", text=student["id"], values=(student["studentCode"], student["name"]))

    def handleAdd(self):
        studentId = self.student.get()
        response = enrollmentAPI.addEnrollment(self.scheduleId, studentId)

        if response["success"]:
            self.addRecord(response["data"][0])
        else:
            messagebox.showerror("Lỗi", response["message"])

    def addRecord(self, data):
        self.tree.insert("", "end", text=data["id"], values=(data["studentCode"], data["name"]))

    def deleteRecord(self, event):
        item = event.widget.selection()[0]
        studentId = self.tree.item(item, "text")
        studentCode = self.tree.item(item, "values")[0]
        print("enrollment id", studentId, self.scheduleId)

        if messagebox.askyesno("Xác nhận", f"Xác nhận xóa sinh viên {studentCode} khỏi lớp"):
            response = enrollmentAPI.deleteEnrollment(studentId, self.scheduleId)

            if response["success"]:
                self.tree.delete(item)
            else:
                messagebox.showerror("Lỗi", response["message"])
