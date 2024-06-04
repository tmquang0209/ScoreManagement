from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

from API import year as yearAPI, semester as semesterAPI, subject as subjectAPI, schedule as scheduleAPI, score as scoreAPI, enrollment as enrollmentAPI, student as studentAPI

class Enrollment(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.initUI()

    def initData(self):
        self.years = yearAPI.getAllYears()["data"] if "data" in yearAPI.getAllYears() else []
        self.subjects = subjectAPI.getAllSubjects()["data"] if "data" in subjectAPI.getAllSubjects() else []
        self.students = studentAPI.getAllStudents()["data"] if "data" in studentAPI.getAllStudents() else []

        self.yearCombobox.set("")
        self.yearCombobox["values"] = [year["year"] for year in self.years]

        self.subjectCombobox.set("")
        self.subjectCombobox["values"] = [subject["subjectName"] for subject in self.subjects]

        self.studentCombobox.set("")
        self.studentCombobox["values"] = [f"{student['studentCode']} - {student['name']}" for student in self.students]

    def initUI(self):
        self.enrollmentContainer = Frame(self)
        self.enrollmentContainer.pack(pady=20, side=LEFT, fill=BOTH, expand=True)

        self.scoreContainer = Frame(self)
        self.scoreContainer.pack(pady=20, side=LEFT, fill=BOTH, expand=True)

        self.createFormUI()
        self.createTreeViewUI()
        self.createScoreUI()
        self.createEnrollmentUI()

    def createFormUI(self):
        self.form = Frame(self.enrollmentContainer)
        self.form.pack(pady=20)

        self.years = []
        self.semesters = []
        self.subjects = []

        Label(self.form, text="Năm học").grid(row=0, column=0, padx=5, pady=5)
        self.yearCombobox = Combobox(self.form, state="readonly")
        self.yearCombobox.grid(row=0, column=1, padx=5, pady=5)
        self.yearCombobox.bind("<<ComboboxSelected>>", self.onYearChange)

        Label(self.form, text="Học kỳ").grid(row=0, column=2, padx=5, pady=5)
        self.semesterCombobox = Combobox(self.form)
        self.semesterCombobox.grid(row=0, column=3, padx=5, pady=5)

        Label(self.form, text="Môn học").grid(row=1, column=0, padx=5, pady=5)
        self.subjectCombobox = Combobox(self.form, state="readonly")
        self.subjectCombobox.grid(row=1, column=1, padx=5, pady=5)

        Label(self.form, text="Lớp").grid(row=1, column=2, padx=5, pady=5)
        self.classNameEntry = Entry(self.form)
        self.classNameEntry.grid(row=1, column=3, padx=5, pady=5)

        Button(self.form, text="Tìm kiếm", command=self.handleSearch).grid(row=2, columnspan=4, column=0, padx=5, pady=5)

    def createTreeViewUI(self):
        self.tree = Treeview(self.enrollmentContainer, columns=("#1", "#2"), show="headings")
        self.tree.pack(pady=20)

        self.tree.column("#1", anchor=CENTER)
        self.tree.heading("#1", text="Lớp")

        self.tree.column("#2", anchor=CENTER)
        self.tree.heading("#2", text="Số lượng sinh viên")

        self.tree.bind("<<TreeviewSelect>>", self.viewRecords)

    def createScoreUI(self):
        def handleOpenCreateScore():
            if self.scheduleId:
                self.controller.screens["ScoreCreate"].initData(self.scheduleId)
                self.controller.showFrame("ScoreCreate", self.scheduleId)
            else:
                messagebox.showerror("Lỗi", "Vui lòng chọn lịch học")

        self.scoreFrame = Frame(self.scoreContainer)
        self.scoreFrame.pack(pady=20)

        Button(self.scoreFrame, text="Nhập điểm", command=handleOpenCreateScore).pack(pady=20)

        self.scoreTree = Treeview(self.scoreFrame, columns=("#1", "#2", "#3", "#4", "#5"), show="headings")

        self.scoreTree.column("#1", width=100, anchor=CENTER)
        self.scoreTree.heading("#1", text="Mã sinh viên")

        self.scoreTree.column("#2", width=150, anchor=CENTER)
        self.scoreTree.heading("#2", text="Tên sinh viên")

        self.scoreTree.column("#3", width=100, anchor=CENTER)
        self.scoreTree.heading("#3", text="Điểm giữa kỳ")

        self.scoreTree.column("#4", width=100, anchor=CENTER)
        self.scoreTree.heading("#4", text="Điểm cuối kỳ")

        self.scoreTree.column("#5", width=100, anchor=CENTER)
        self.scoreTree.heading("#5", text="Điểm trung bình")

        self.scoreTree.pack(pady=20)
        self.scoreTree.bind("<Double-1>", self.editScore)

    def createEnrollmentUI(self):
        self.enrollmentFrame = Frame(self.scoreContainer)
        self.enrollmentFrame.pack(pady=20)

        self.enrollmentForm = Frame(self.enrollmentFrame)
        self.enrollmentForm.pack(pady=20)

        Label(self.enrollmentForm, text="Sinh viên").grid(row=0, column=0, padx=5, pady=5)
        self.studentCombobox = Combobox(self.enrollmentForm)
        self.studentCombobox.grid(row=0, column=1, padx=5, pady=5)

        Button(self.enrollmentForm, text="Thêm", command=self.handleAddEnrollment).grid(row=0, column=2, padx=5, pady=5)

        self.enrollmentTree = Treeview(self.enrollmentFrame, columns=("#1", "#2"), show="headings")
        self.enrollmentTree.pack(pady=20)

        self.enrollmentTree.column("#1", anchor=CENTER)
        self.enrollmentTree.heading("#1", text="Mã sinh viên")

        self.enrollmentTree.column("#2", anchor=CENTER)
        self.enrollmentTree.heading("#2", text="Họ tên")

        self.enrollmentTree.bind("<Delete>", self.deleteEnrollmentRecord)

    def onYearChange(self, event):
        yearValue = self.yearCombobox.current()
        year = self.years[yearValue] if yearValue != -1 else ""
        self.semesters = semesterAPI.getSemesterByYear(year["id"])["data"] if "data" in semesterAPI.getSemesterByYear(year["id"]) else []

        self.semesterCombobox.set("")
        self.semesterCombobox["values"] = [semesters["semester"] for semesters in self.semesters]

    def handleSearch(self):
        yearValue = self.yearCombobox.current()
        semesterValue = self.semesterCombobox.current()
        subjectValue = self.subjectCombobox.current()

        year = self.years[yearValue] if yearValue != -1 else ""
        semester = self.semesters[semesterValue] if semesterValue != -1 else ""
        subject = self.subjects[subjectValue] if subjectValue != -1 else ""
        className = self.classNameEntry.get()

        if yearValue == -1 or semesterValue == -1:
            messagebox.showerror("Lỗi", "Vui lòng chọn đầy đủ thông tin")
            return

        searchData = {
            "semesterId": semester["id"],
            "subjectId": subject["id"] if subject else "",
            "className": className if className else ""
        }
        schedules = scheduleAPI.searchSchedules(searchData)["data"] if "data" in scheduleAPI.searchSchedules(searchData) else []

        self.updateTreeView(schedules)

    def updateTreeView(self, data):
        self.tree.delete(*self.tree.get_children())
        for schedule in data:
            self.tree.insert("", "end", text=schedule["id"], values=(schedule["className"], schedule["currentStudent"]))

    def viewRecords(self, event):
        item = self.tree.selection()[0]
        self.scheduleId = self.tree.item(item, "text")
        self.showScoreDetails(self.scheduleId)
        self.showEnrollmentDetails(self.scheduleId)

    def showScoreDetails(self, scheduleId):
        scores = scoreAPI.getByScheduleId(scheduleId)["data"] if "data" in scoreAPI.getByScheduleId(scheduleId) else []
        self.updateScoreTreeView(scores)

    def updateScoreTreeView(self, scores):
        self.scoreTree.delete(*self.scoreTree.get_children())
        for score in scores:
            self.scoreTree.insert("", "end", values=(
                score["studentCode"],
                score["studentName"],
                score["midtermScore"],
                score["finalScore"],
                score["score"]
            ))

    def editScore(self, event):
        def handleSave(midtermScore, finalScore, studentCode):
            data = {
                "studentCode": studentCode,
                "midtermTest": midtermScore,
                "finalTest": finalScore
            }

            response = scoreAPI.update(self.scheduleId, data)

            if response["success"]:
                messagebox.showinfo("Thành công", response["message"])
            else:
                messagebox.showerror("Lỗi", response["message"])

            root.destroy()

            self.showScoreDetails(self.scheduleId)

        item = self.scoreTree.selection()[0]
        studentCode = self.scoreTree.item(item, "values")[0]

        studentId = studentAPI.getStudentByCode(studentCode)["data"][0]["id"] if "data" in studentAPI.getStudentByCode(studentCode) else ""

        score = scoreAPI.getByStudentIdAndScheduleId(self.scheduleId, studentId)["data"][0] if "data" in scoreAPI.getByStudentIdAndScheduleId(self.scheduleId, studentId) else ""

        root = Toplevel(self)
        root.title("Chỉnh sửa điểm")

        Label(root, text="Mã sinh viên").grid(row=0, column=0, padx=5, pady=5)
        Label(root, text=studentCode).grid(row=0, column=1, padx=5, pady=5)

        Label(root, text="Tên sinh viên").grid(row=1, column=0, padx=5, pady=5)
        Label(root, text=score["studentName"]).grid(row=1, column=1, padx=5, pady=5)

        Label(root, text="Điểm giữa kỳ").grid(row=2, column=0, padx=5, pady=5)
        midtermScore = Entry(root)
        midtermScore.insert(0, score["midtermScore"])
        midtermScore.grid(row=2, column=1, padx=5, pady=5)

        Label(root, text="Điểm cuối kỳ").grid(row=3, column=0, padx=5, pady=5)
        finalScore = Entry(root)
        finalScore.insert(0, score["finalScore"])
        finalScore.grid(row=3, column=1, padx=5, pady=5)

        Button(root, text="Lưu", command=lambda: handleSave(midtermScore.get(), finalScore.get(), studentCode)).grid(row=4, column=1, padx=5, pady=5)

    def showEnrollmentDetails(self, scheduleId):
        enrollments = enrollmentAPI.getEnrollments(scheduleId)["data"] if "data" in enrollmentAPI.getEnrollments(scheduleId) else []
        print(enrollments)
        self.updateEnrollmentTreeView(enrollments)

    def updateEnrollmentTreeView(self, enrollments):
        self.enrollmentTree.delete(*self.enrollmentTree.get_children())
        for enrollment in enrollments:
            self.enrollmentTree.insert("", "end", values=(enrollment["studentCode"], enrollment["name"]))

    def handleAddEnrollment(self):
        studentValue = self.studentCombobox.current()
        print(studentValue)
        student = self.students[studentValue] if studentValue != -1 else ""

        print(student)

        if studentValue == -1:
            messagebox.showerror("Lỗi", "Vui lòng chọn sinh viên")
            return

        data = {
            "scheduleId": self.scheduleId,
            "studentId": student["id"]
        }

        response = enrollmentAPI.addEnrollment(self.scheduleId, student["id"])

        if response["success"]:
            messagebox.showinfo("Thành công", response["message"])
        else:
            messagebox.showerror("Lỗi", response["message"])

        self.showEnrollmentDetails(self.scheduleId)

    def deleteEnrollmentRecord(self, event):
        item = self.enrollmentTree.selection()[0]
        studentCode = self.enrollmentTree.item(item, "values")[0]

        studentId = studentAPI.getStudentByCode(studentCode)["data"][0]["id"] if "data" in studentAPI.getStudentByCode(studentCode) else ""

        response = enrollmentAPI.delete(self.scheduleId, studentId)

        if response["success"]:
            messagebox.showinfo("Thành công", response["message"])
        else:
            messagebox.showerror("Lỗi", response["message"])

        self.showEnrollmentDetails(self.scheduleId)
