from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

from API import schedule as scheduleAPI, score as scoreAPI, enrollment as enrollmentAPI
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

        self.semesterId = scheduleDetails["semester"]["id"]
        self.subjectId = scheduleDetails["subject"]["id"]

        studentsList = enrollmentAPI.getEnrollments(scheduleId)["data"] if "data" in enrollmentAPI.getEnrollments(scheduleId) else []

        existsList = scoreAPI.getByScheduleId(scheduleId)["data"] if "data" in scoreAPI.getByScheduleId(scheduleId) else []

        reduceList = []

        for student in studentsList:
            for exists in existsList:
                if student["studentCode"] == exists["studentCode"]:
                    break
            else:
                reduceList.append(student)

        self.insertData(reduceList)

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
            self.controller.showFrame("Enrollment")
        else:
            messagebox.showerror("Lỗi", response["message"])