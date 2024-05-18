from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

from API import schedule as scheduleAPI, semester as semesterAPI, subject as subjectAPI, year as yearAPI, major as majorAPI, teacher as teacherAPI

class Schedule(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.initUI()

    def initUI(self):
        self.scheduleLabel = Label(self, text="Quản lý lịch học", font=("Helvetica", 18))
        self.scheduleLabel.pack(side="top", fill="x", pady=10, padx=10)

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

    def updateTree(self, schedule):
        self.tree.selection()[0]
        self.tree.item(self.tree.selection()[0], text=schedule["id"], values=(schedule["subject"]["subjectName"], schedule["className"], schedule["room"], schedule["day"], schedule["shift"], schedule["maxStudent"], schedule["currentStudent"], schedule["teacher"]["name"]))

    def insertItemToTree(self, schedule):
        self.tree.insert("", "end", text=schedule["id"], values=(schedule["subject"]["subjectName"], schedule["className"], schedule["room"], schedule["day"], schedule["shift"], schedule["maxStudent"], schedule["currentStudent"], schedule["teacher"]["name"]))

    def initData(self):
        # clear tree
        for i in self.tree.get_children():
            self.tree.delete(i)

        response = scheduleAPI.getAllSchedules()

        if "success" in response and response["success"]:
            self.scheduleList = response["data"]
            for schedule in self.scheduleList:
                self.insertItemToTree(schedule)
        else:
            messagebox.showerror("Error", response["message"])

    def editSchedule(self, event, scheduleAPI=scheduleAPI, subjectAPI=subjectAPI, majorAPI=majorAPI, teacherAPI=teacherAPI, semesterAPI=semesterAPI):
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
        root.geometry("500x500")

        id = event.widget.item(event.widget.selection()[0])["text"]
        schedule = event.widget.item(event.widget.selection()[0])["values"]

        subjectsList = subjectAPI.getAllSubjects()["data"] if "success" in subjectAPI.getAllSubjects() and subjectAPI.getAllSubjects()["success"] else []

        semestersList = semesterAPI.getAllSemesters()["data"] if "success" in semesterAPI.getAllSemesters() and semesterAPI.getAllSemesters()["success"] else []

        majorsList = majorAPI.getAllMajors()["data"] if "success" in majorAPI.getAllMajors() and majorAPI.getAllMajors()["success"] else []

        teachersList = teacherAPI.getAllTeachers()["data"] if "success" in teacherAPI.getAllTeachers() and teacherAPI.getAllTeachers()["success"] else []

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
            "subject": subjectsList[subject.current()],
            "className": class_.get(),
            "room": room.get(),
            "day": day.get(),
            "shift": shift.get(),
            "maxStudent": maxStudent.get(),
            "teacher": teachersList[teacher.current()]
        })).grid(row=7, column=0, columnspan=2, pady=10)

    def deleteSchedule(self, event, scheduleAPI=scheduleAPI):
        response = scheduleAPI.deleteSchedule(event.widget.item(event.widget.selection()[0])["text"])

        if "success" in response and response["success"]:
            messagebox.showinfo("Success", response["message"])
            self.initData()
        else:
            messagebox.showerror("Error", response["message"])


class ScheduleCreate(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.initUI()

    def initUI(self):
        self.scheduleLabel = Label(self, text="Thêm lịch học mới", font=("Helvetica", 18))
        self.scheduleLabel.pack(side="top", fill="x", pady=10, padx=10)

        subjectsList = subjectAPI.getAllSubjects()["data"] if "success" in subjectAPI.getAllSubjects() and subjectAPI.getAllSubjects()["success"] else []

        semestersList = semesterAPI.getAllSemesters()["data"] if "success" in semesterAPI.getAllSemesters() and semesterAPI.getAllSemesters()["success"] else []

        majorsList = majorAPI.getAllMajors()["data"] if "success" in majorAPI.getAllMajors() and majorAPI.getAllMajors()["success"] else []

        teachersList = teacherAPI.getAllTeachers()["data"] if "success" in teacherAPI.getAllTeachers() and teacherAPI.getAllTeachers()["success"] else []

        Label(self, text="Kỳ học").pack()
        self.semester = Combobox(self, values=[semester["semester"] for semester in semestersList])
        self.semester.pack()

        Label(self, text="Chuyên ngành").pack()
        self.major = Combobox(self, values=[major["majorName"] for major in majorsList])
        self.major.pack()

        Label(self, text="Tên môn học").pack()
        self.subject = Combobox(self, values=[subject["subjectName"] for subject in subjectsList])
        self.subject.pack()

        Label(self, text="Tên lớp").pack()
        self.class_ = Entry(self)
        self.class_.pack()

        Label(self, text="Phòng học").pack()
        self.room = Entry(self)
        self.room.pack()

        Label(self, text="Thứ").pack()
        self.day = Entry(self)
        self.day.pack()

        Label(self, text="Giờ học").pack()
        self.shift = Entry(self)
        self.shift.pack()

        Label(self, text="Số lượng tối đa").pack()
        self.maxStudent = Entry(self)
        self.maxStudent.pack()

        Label(self, text="Giảng viên").pack()
        self.teacher = Combobox(self, values=[teacher["name"] for teacher in teachersList])
        self.teacher.pack()

        Button(self, text="Thêm", command=lambda: self.handleCreateSchedule(
                                                                    semestersList[self.semester.current()],
                                                                    majorsList[self.major.current()],
                                                                    subjectsList[self.subject.current()],
                                                                    self.class_.get(),
                                                                    self.room.get(),
                                                                    self.day.get(),
                                                                    self.shift.get(),
                                                                    self.maxStudent.get(),
                                                                    teachersList[self.teacher.current()])).pack()

    def handleCreateSchedule(self, semester, major, subject, class_, room, day, shift, maxStudent, teacher):
        response = scheduleAPI.createSchedule({
            "semester": semester,
            "major": major,
            "subject": subject,
            "className": class_,
            "room": room,
            "day": day,
            "shift": shift,
            "maxStudent": maxStudent,
            "currentStudent": 0,
            "teacher": teacher
        })

        if "success" in response and response["success"]:
            messagebox.showinfo("Success", response["message"])
            self.controller.screens["Schedule"].initData()
            self.controller.showFrame("Schedule")
        else:
            messagebox.showerror("Error", response["message"])