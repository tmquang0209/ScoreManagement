from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

from API import schedule as scheduleAPI, semester as semesterAPI, subject as subjectAPI, year as yearAPI, major as majorAPI, teacher as teacherAPI

class Schedule(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.initUI()

    def onYearChange(self, event):
        year = self.yearsList[self.year.current()]
        self.semesters = semesterAPI.getSemesterByYear(year["id"])["data"] if "success" in semesterAPI.getSemesterByYear(year["id"]) and semesterAPI.getSemesterByYear(year["id"])["success"] else []

        self.semester.set("")
        self.semester["values"] = [semester["semester"] for semester in self.semesters]

        self.createSemester.set("")
        self.createSemester["values"] = [semester["semester"] for semester in self.semesters]


    def initUI(self):
        self.createForm()

        self.scheduleLabel = Label(self, text="Quản lý lịch học", font=("Helvetica", 18))
        self.scheduleLabel.pack(side="top", fill="x", pady=10, padx=10)

        formFrame = Frame(self)
        formFrame.pack(pady=10)

        self.semesters = []
        self.yearsList = yearAPI.getAllYears()["data"] if "success" in yearAPI.getAllYears() and yearAPI.getAllYears()["success"] else []

        Label(formFrame, text="Năm học").grid(row=0, column=0, padx=5, pady=10)
        self.year = Combobox(formFrame, values=[year["year"] for year in self.yearsList])
        self.year.grid(row=0, column=1, padx=5, pady=10)
        self.createYear.bind("<<ComboboxSelected>>", self.onYearChange)

        Label(formFrame, text="Kỳ học").grid(row=0, column=3, padx=5, pady=10)
        self.semester = Combobox(formFrame, values=[])
        self.semester.grid(row=0, column=4, padx=5, pady=10)

        Label(formFrame, text="Tên lớp").grid(row=0, column=6, padx=5, pady=10)
        self.className = Entry(formFrame)
        self.className.grid(row=0, column=7, padx=5, pady=10)

        Button(formFrame, text="Tìm kiếm", command=self.handleSearch).grid(row=0, column=8, padx=5, pady=10)

        self.columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8")
        self.tree = Treeview(self, columns=self.columns, show="headings")
        self.tree.heading("#1", text="Tên môn học")
        self.tree.heading("#2", text="Tên lớp")
        self.tree.column("#3", width=50)
        self.tree.heading("#3", text="Phòng học")
        self.tree.column("#4", width=50)
        self.tree.heading("#4", text="Thứ")
        self.tree.column("#5", width=50)
        self.tree.heading("#5", text="Giờ học")
        self.tree.column("#6", width=80)
        self.tree.heading("#6", text="SL tối đa")
        self.tree.column("#7", width=80)
        self.tree.heading("#7", text="SL hiện tại")
        self.tree.heading("#8", text="Giảng viên")
        self.tree.bind("<Double-1>", self.editSchedule)
        self.tree.bind("<Delete>", self.deleteSchedule)
        self.tree.pack(padx=10)

    def createForm(self):
                # Form for creating a new schedule
        self.createForm = LabelFrame(self, text="Thêm lịch học mới")
        self.createForm.pack(fill="x", padx=10, pady=10)

        self.yearsList = yearAPI.getAllYears()["data"] if "success" in yearAPI.getAllYears() and yearAPI.getAllYears()["success"] else []
        subjectsList = subjectAPI.getAllSubjects()["data"] if "success" in subjectAPI.getAllSubjects() and subjectAPI.getAllSubjects()["success"] else []
        majorsList = majorAPI.getAllMajors()["data"] if "success" in majorAPI.getAllMajors() and majorAPI.getAllMajors()["success"] else []
        teachersList = teacherAPI.getAllTeachers()["data"] if "success" in teacherAPI.getAllTeachers() and teacherAPI.getAllTeachers()["success"] else []

        Label(self.createForm, text="Năm học").grid(row=0, column=0)
        self.createYear = Combobox(self.createForm, values=[year["year"] for year in self.yearsList])
        self.createYear.grid(row=0, column=1)
        self.createYear.bind("<<ComboboxSelected>>", self.onYearChange)

        Label(self.createForm, text="Kỳ học").grid(row=0, column=2, padx=5, pady=10)
        self.createSemester = Combobox(self.createForm)
        self.createSemester.grid(row=0, column=3, padx=5, pady=10)

        Label(self.createForm, text="Chuyên ngành").grid(row=0, column=4, padx=5, pady=10)
        self.createMajor = Combobox(self.createForm, values=[major["majorName"] for major in majorsList])
        self.createMajor.grid(row=0, column=5, padx=5, pady=10)

        Label(self.createForm, text="Tên môn học").grid(row=0, column=6, padx=5, pady=10)
        self.createSubject = Combobox(self.createForm, values=[subject["subjectName"] for subject in subjectsList])
        self.createSubject.grid(row=0, column=7, padx=5, pady=10)

        Label(self.createForm, text="Tên lớp").grid(row=0, column=8)
        self.createClass = Entry(self.createForm)
        self.createClass.grid(row=0, column=9)

        Label(self.createForm, text="Phòng học").grid(row=1, column=0)
        self.createRoom = Entry(self.createForm)
        self.createRoom.grid(row=1, column=1)

        Label(self.createForm, text="Thứ").grid(row=1, column=2)
        self.createDay = Entry(self.createForm)
        self.createDay.grid(row=1, column=3)

        Label(self.createForm, text="Giờ học").grid(row=1, column=4)
        self.createShift = Entry(self.createForm)
        self.createShift.grid(row=1, column=5)

        Label(self.createForm, text="Số lượng tối đa").grid(row=1, column=6)
        self.createMaxStudent = Entry(self.createForm)
        self.createMaxStudent.grid(row=1, column=7)

        Label(self.createForm, text="Giảng viên").grid(row=1, column=8)
        self.createTeacher = Combobox(self.createForm, values=[teacher["name"] for teacher in teachersList])
        self.createTeacher.grid(row=1, column=9)

        Button(self.createForm, text="Thêm", command=self.handleCreateSchedule).grid(row=2, column=0, columnspan=2, pady=10)

        Button(self.createForm, text="Hủy", command=self.clearForm).grid(row=2, column=2, columnspan=2, pady=10)

    def clearForm(self):
        self.createYear.set("")
        self.createSemester.set("")
        self.createMajor.set("")
        self.createSubject.set("")
        self.createClass.delete(0, END)
        self.createRoom.delete(0, END)
        self.createDay.delete(0, END)
        self.createShift.delete(0, END)
        self.createMaxStudent.delete(0, END)
        self.createTeacher.set("")

    def updateTree(self, schedule):
        selected_item = self.tree.selection()[0]
        self.tree.item(selected_item, text=schedule["id"], values=(schedule["subject"]["subjectName"], schedule["className"],
                                                                   schedule["room"], schedule["day"], schedule["shift"],
                                                                   schedule["maxStudent"], schedule["currentStudent"],
                                                                   schedule["teacher"]["name"]))

    def insertItemToTree(self, schedule):
        self.tree.insert("", "end", text=schedule["id"], values=(schedule["subject"]["subjectName"], schedule["className"],
                                                                 schedule["room"], schedule["day"], schedule["shift"],
                                                                 schedule["maxStudent"], schedule["currentStudent"],
                                                                 schedule["teacher"]["name"]))

    def handleSearch(self):
        semesterId = self.semesters[self.semester.current()]["id"] if self.semester.get() else None
        response = scheduleAPI.searchSchedules({
            "semesterId": semesterId,
            "className": self.className.get()
        })

        if "success" in response and response["success"]:
            for i in self.tree.get_children():
                self.tree.delete(i)
            self.scheduleList = response["data"]
            for schedule in self.scheduleList:
                self.insertItemToTree(schedule)
        else:
            messagebox.showerror("Error", response["message"])

    def initData(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        response = scheduleAPI.getAllSchedules()

        if "success" in response and response["success"]:
            self.scheduleList = response["data"]
            for schedule in self.scheduleList:
                self.insertItemToTree(schedule)
        else:
            messagebox.showerror("Error", response["message"])

    def handleCreateSchedule(self):
        semester = self.semesters[self.createSemester.current()] if self.createSemester.get() else None
        major = majorAPI.getAllMajors()["data"][self.createMajor.current()] if self.createMajor.get() else None
        subject = subjectAPI.getAllSubjects()["data"][self.createSubject.current()] if self.createSubject.get() else None
        teacher = teacherAPI.getAllTeachers()["data"][self.createTeacher.current()] if self.createTeacher.get() else None

        data = {
            "semester": semester,
            "major": major,
            "subject": subject,
            "className": self.createClass.get(),
            "room": self.createRoom.get(),
            "day": self.createDay.get(),
            "shift": self.createShift.get(),
            "maxStudent": self.createMaxStudent.get(),
            "currentStudent": 0,
            "teacher": teacher
        }

        response = scheduleAPI.createSchedule(data)
        if "success" in response and response["success"]:
            messagebox.showinfo("Success", response["message"])
            self.initData()
            self.clearForm()
        else:
            messagebox.showerror("Error", response["message"])

    def editSchedule(self, event):
        def handleUpdateSchedule(id, data):
            response = scheduleAPI.updateSchedule(id, data)
            if "success" in response and response["success"]:
                messagebox.showinfo("Success", response["message"])
                self.initData()
                root.destroy()
            else:
                messagebox.showerror("Error", response["message"])

        root = Toplevel()
        root.title("Chỉnh sửa lịch học")

        id = event.widget.item(event.widget.selection()[0])["text"]
        schedule = event.widget.item(event.widget.selection()[0])["values"]

        subjectsList = subjectAPI.getAllSubjects()["data"] if "success" in subjectAPI.getAllSubjects() and subjectAPI.getAllSubjects()["success"] else []
        majorsList = majorAPI.getAllMajors()["data"] if "success" in majorAPI.getAllMajors() and majorAPI.getAllMajors()["success"] else []
        teachersList = teacherAPI.getAllTeachers()["data"] if "success" in teacherAPI.getAllTeachers() and teacherAPI.getAllTeachers()["success"] else []

        Label(root, text="Chuyên ngành").grid(row=0, column=2)
        major = Combobox(root, values=[major["majorName"] for major in majorsList])
        major.grid(row=0, column=3)

        Label(root, text="Tên môn học").grid(row=0, column=0)
        subject = Combobox(root, values=[subject["subjectName"] for subject in subjectsList])
        subject.set(schedule[0])
        subject.grid(row=0, column=1)

        Label(root, text="Tên lớp").grid(row=1, column=0, padx=5, pady=10)
        class_ = Entry(root)
        class_.insert(0, schedule[1])
        class_.grid(row=1, column=1, padx=5, pady=10)

        Label(root, text="Phòng học").grid(row=2, column=0, padx=5, pady=10)
        room = Entry(root)
        room.insert(0, schedule[2])
        room.grid(row=2, column=1, padx=5, pady=10)

        Label(root, text="Thứ").grid(row=3, column=0, padx=5, pady=10)
        day = Entry(root)
        day.insert(0, schedule[3])
        day.grid(row=3, column=1, padx=5, pady=10)

        Label(root, text="Giờ học").grid(row=4, column=0, padx=5, pady=10)
        shift = Entry(root)
        shift.insert(0, schedule[4])
        shift.grid(row=4, column=1, padx=5, pady=10)

        Label(root, text="Số lượng tối đa").grid(row=5, column=0, padx=5, pady=10)
        maxStudent = Entry(root)
        maxStudent.insert(0, schedule[5])
        maxStudent.grid(row=5, column=1, padx=5, pady=10)

        Label(root, text="Giảng viên").grid(row=6, column=0, padx=5, pady=10)
        teacher = Combobox(root, values=[teacher["name"] for teacher in teachersList])
        teacher.set(schedule[7])
        teacher.grid(row=6, column=1, padx=5, pady=10)

        Button(root, text="Cập nhật", command=lambda: handleUpdateSchedule(id, {
            "major": majorsList[major.current()],
            "subject": subjectsList[subject.current()],
            "className": class_.get(),
            "room": room.get(),
            "day": day.get(),
            "shift": shift.get(),
            "maxStudent": maxStudent.get(),
            "teacher": teachersList[teacher.current()]
        })).grid(row=7, column=0, columnspan=2, pady=10)

    def deleteSchedule(self, event):
        response = scheduleAPI.deleteSchedule(event.widget.item(event.widget.selection()[0])["text"])

        if "success" in response and response["success"]:
            messagebox.showinfo("Success", response["message"])
            self.initData()
        else:
            messagebox.showerror("Error", response["message"])
