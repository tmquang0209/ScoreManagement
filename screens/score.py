from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

from API import year as yearAPI, semester as semesterAPI, subject as subjectAPI, schedule as scheduleAPI, score as scoreAPI, enrollment as enrollmentAPI, student as studentAPI

class Score(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.initUI()

    def initUI(self):
        self.form = Frame(self)
        self.form.pack()

        self.years = []
        self.semesters = []
        self.subjects = []

        Label(self.form, text="Năm học").grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.yearCombobox = Combobox(self.form, state="readonly")
        self.yearCombobox.grid(row=0, column=1, sticky=W, padx=5, pady=5)
        self.yearCombobox.bind("<<ComboboxSelected>>", self.onYearChange)

        Label(self.form, text="Học kỳ").grid(row=0, column=3, sticky=W, padx=5, pady=5)
        self.semesterCombobox = Combobox(self.form)
        self.semesterCombobox.grid(row=0, column=4, sticky=W, padx=5, pady=5)

        Label(self.form, text="Môn học").grid(row=0, column=6, sticky=W, padx=5, pady=5)
        self.subjectCombobox = Combobox(self.form, state="readonly")
        self.subjectCombobox.grid(row=0, column=7, sticky=W, padx=5, pady=5)

        Button(self.form, text="Tìm kiếm", command=self.handleViewScore).grid(row=0, column=8, sticky=W, padx=5, pady=5)

        # tree
        columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7")
        self.tree = Treeview(self, columns=columns, show="headings")
        self.tree.pack()

        self.tree.column("#1", width=80, anchor=CENTER)
        self.tree.heading("#1", text="Mã môn học")

        self.tree.column("#2", width=150, anchor=CENTER)
        self.tree.heading("#2", text="Tên môn học")

        self.tree.column("#3", width=150, anchor=CENTER)
        self.tree.heading("#3", text="Tên lớp")

        self.tree.column("#4", width=80, anchor=CENTER)
        self.tree.heading("#4", text="Phòng học")

        self.tree.column("#5", width=80, anchor=CENTER)
        self.tree.heading("#5", text="Thứ")

        self.tree.column("#6", width=80, anchor=CENTER)
        self.tree.heading("#6", text="Giờ học")

        self.tree.column("#7", width=80, anchor=CENTER)
        self.tree.heading("#7", text="Sỹ số")

        self.tree.bind("<Double-1>", self.handleDoubleClick)
    def handleDoubleClick(self, event):
        item = self.tree.selection()[0]
        scheduleId = self.tree.item(item, "text")
        self.controller.screens["ScoreDetail"].initData(scheduleId)
        self.controller.showFrame("ScoreDetail", scheduleId)

    def insertData(self, schedules):
        self.tree.delete(*self.tree.get_children())
        for schedule in schedules:
            self.tree.insert("", "end", text=schedule["id"], values=(
                schedule["subject"]["subjectCode"],
                schedule["subject"]["subjectName"],
                schedule["className"],
                schedule["room"],
                schedule["day"],
                schedule["shift"],
                schedule["currentStudent"]
            ))

    def initData(self):
        self.years = yearAPI.getAllYears()["data"] if "data" in yearAPI.getAllYears() else []
        self.subjects = subjectAPI.getAllSubjects()["data"] if "data" in subjectAPI.getAllSubjects() else []

        self.yearCombobox["values"] = [year["year"] for year in self.years]
        self.subjectCombobox["values"] = [subject["subjectName"] for subject in self.subjects]

    def onYearChange(self, event):
        yearValue = self.yearCombobox.current()

        year = self.years[yearValue] if yearValue != -1 else ""

        self.semesters = semesterAPI.getSemesterByYear(year["id"])["data"] if "data" in semesterAPI.getSemesterByYear(year["id"]) else []


        self.semesterCombobox.set("")
        self.semesterCombobox["values"] = [semesters["semester"] for semesters in self.semesters]

    def handleViewScore(self):
        yearValue = self.yearCombobox.current()
        semesterValue = self.semesterCombobox.current()
        subjectValue = self.subjectCombobox.current()

        year = self.years[yearValue] if yearValue != -1 else ""
        semester = self.semesters[semesterValue] if semesterValue != -1 else ""
        subject = self.subjects[subjectValue] if subjectValue != -1 else ""

        print(year, semester, subject)

        if yearValue == -1 or semesterValue == -1:
            messagebox.showerror("Lỗi", "Vui lòng chọn đầy đủ thông tin")
            return

        searchData = {
            "semesterId": semester["id"],
            "subjectId": subject["id"] if subject else "",
        }
        schedules = scheduleAPI.getScheduleForTeacher(searchData)["data"] if "data" in scheduleAPI.getScheduleForTeacher(searchData) else []

        self.insertData(schedules)

class ScoreDetail(Frame):
    def __init__(self, parent, controller, scheduleId):
        super().__init__(parent)
        self.controller = controller
        self.scheduleId = scheduleId

        self.initUI()

    def initUI(self):
        def handleOpenCreateScore():
            self.controller.screens["ScoreCreate"].initData(self.scheduleId)
            self.controller.showFrame("ScoreCreate", self.scheduleId)
        Button(self, text="Nhập điểm", command=handleOpenCreateScore).pack(padx=5, pady=5)

        columns = ("#1", "#2", "#3", "#4", "#5")
        self.tree = Treeview(self, columns=columns, show="headings")

        self.tree.pack()

        self.tree.column("#1", width=100, anchor=CENTER)
        self.tree.heading("#1", text="Mã sinh viên")

        self.tree.column("#2", width=150, anchor=CENTER)
        self.tree.heading("#2", text="Tên sinh viên")

        self.tree.column("#3", width=100, anchor=CENTER)
        self.tree.heading("#3", text="Điểm giữa kỳ")

        self.tree.column("#4", width=100, anchor=CENTER)
        self.tree.heading("#4", text="Điểm cuối kỳ")

        self.tree.column("#5", width=100, anchor=CENTER)
        self.tree.heading("#5", text="Điểm trung bình")

        self.tree.bind("<Double-1>", self.editScore)

    def insertData(self, scores):
        self.tree.delete(*self.tree.get_children())
        for score in scores:
            self.tree.insert("", "end", values=(
                score["studentCode"],
                score["studentName"],
                score["midtermScore"],
                score["finalScore"],
                score["score"]
            ))

    def initData(self, scheduleId):
        self.scheduleId = scheduleId
        scores = scoreAPI.getByScheduleId(scheduleId)["data"] if "data" in scoreAPI.getByScheduleId(scheduleId) else []
        self.insertData(scores)

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

            self.controller.screens["ScoreDetail"].initData(self.scheduleId)

        item = self.tree.selection()[0]
        studentCode = self.tree.item(item, "values")[0]

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

        Button(root, text="Lưu", command=lambda: handleSave(
            midtermScore.get(),
            finalScore.get(),
            studentCode
        )).grid(row=4, column=1, padx=5, pady=5)

class ScoreCreate(Frame):
    def __init__(self, parent, controller, scheduleId):
        super().__init__(parent)
        self.controller = controller
        self.scheduleId = scheduleId
        self.semesterId = None
        self.subjectId = None

        self.initUI()

    def initUI(self):
        self.form = Frame(self)
        self.form.pack()

        self.students = []

        Button(self, text="Thêm điểm", command=self.handleCreateScore).pack(padx=5, pady=5)

    def insertData(self, students):
        # delete all child in form
        for widget in self.form.winfo_children():
            widget.destroy()

        Label(self.form, text="Mã sinh viên").grid(row=0, column=0, padx=5, pady=5)
        Label(self.form, text="Điểm giữa kỳ").grid(row=0, column=1, padx=5, pady=5)
        Label(self.form, text="Điểm cuối kỳ").grid(row=0, column=2, padx=5, pady=5)

        index = 1
        for student in students:
            Label(self.form, text=student["studentCode"]).grid(row=index, column=0, padx=5, pady=5)
            Spinbox(self.form, name=f"midTerm_{index}").grid(row=index, column=1, padx=5, pady=5)
            Spinbox(self.form, name=f"final_{index}").grid(row=index, column=2, padx=5, pady=5)

            index += 1

    def initData(self, scheduleId):
        self.scheduleId = scheduleId
        scheduleDetails = scheduleAPI.getScheduleById(scheduleId)["data"][0] if "data" in scheduleAPI.getScheduleById(scheduleId) else []

        print(scheduleDetails)

        self.semesterId = scheduleDetails["semester"]["id"]
        self.subjectId = scheduleDetails["subject"]["id"]

        studentsList = enrollmentAPI.getEnrollments(scheduleId)["data"] if "data" in enrollmentAPI.getEnrollments(scheduleId) else []

        print(studentsList)
        self.insertData(studentsList)

    def handleCreateScore(self):
        entries = self.form.winfo_children()
        data = []

        student_entries = {}

        for widget in entries:
            if isinstance(widget, Label) and widget.grid_info()["row"] > 0:  # skip header labels
                row = widget.grid_info()["row"]
                studentCode = widget.cget("text")
                student_entries[row] = {"studentCode": studentCode}
            elif isinstance(widget, Spinbox):
                row = widget.grid_info()["row"]
                col = widget.grid_info()["column"]
                if col == 1:
                    student_entries[row]["midtermTest"] = widget.get()
                elif col == 2:
                    student_entries[row]["finalTest"] = widget.get()

        # Convert dictionary to list of dictionaries
        for row in sorted(student_entries.keys()):
            data.append(student_entries[row])

        response = scoreAPI.create(self.semesterId, self.subjectId, data)

        if response["success"]:
            messagebox.showinfo("Thành công", response["message"])
        else:
            messagebox.showerror("Lỗi", response["message"])