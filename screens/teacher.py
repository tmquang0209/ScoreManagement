from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkcalendar import Calendar

from API import major as majorAPI, teacher as teacherAPI

class Teacher(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.majorsList = majorAPI.getAllMajors()["data"] if majorAPI.getAllMajors()["success"] else []
        self.initUI()

    def initUI(self):
        title = Label(self, text="Danh sách giáo viên", font=("Helvetica", 18))
        title.pack(side="top", fill="x", pady=10, padx=10)

        self.createForm()
        self.createTreeView()

    def createForm(self):
        formFrame = Frame(self)
        formFrame.pack(padx=10, pady=10, fill="x")

        Label(formFrame, text="Mã giáo viên").grid(row=0, column=0)
        self.teacherCode = Entry(formFrame)
        self.teacherCode.grid(row=0, column=1, padx=5, pady=10)

        Label(formFrame, text="Tên giáo viên").grid(row=0, column=2)
        self.name = Entry(formFrame)
        self.name.grid(row=0, column=3, padx=5, pady=10)

        Label(formFrame, text="Email").grid(row=0, column=5)
        self.email = Entry(formFrame)
        self.email.grid(row=0, column=6, padx=5, pady=10)

        Label(formFrame, text="Số điện thoại").grid(row=0, column=7)
        self.phone = Entry(formFrame)
        self.phone.grid(row=0, column=8, padx=5, pady=10)

        Label(formFrame, text="Địa chỉ").grid(row=1, column=0)
        self.address = Entry(formFrame)
        self.address.grid(row=1, column=1, padx=5, pady=10)

        Label(formFrame, text="Ngày sinh").grid(row=1, column=2)
        self.dob = Entry(formFrame)
        self.dob.config(state="readonly")
        self.dob.grid(row=1, column=3, padx=5, pady=10)

        dobBtn = Button(formFrame, text="Chọn ngày", command=lambda: self.openCalendar(self.dob, self.dob.get() if self.dob.get() != "" else None))
        dobBtn.grid(row=1, column=4, padx=5, pady=10)

        Label(formFrame, text="Giới tính").grid(row=1, column=6, padx=5, pady=10)
        self.gender = Combobox(formFrame, values=["Male", "Female"])
        self.gender.grid(row=1, column=7, padx=5, pady=10)

        Label(formFrame, text="Khoa/ Phòng ban").grid(row=1, column=8)
        self.major = Combobox(formFrame, values=[major["majorName"] for major in self.majorsList])
        self.major.grid(row=1, column=9, padx=5, pady=10)

        submitBtn = Button(formFrame, text="Thêm giáo viên", command=self.handleCreateTeacher)
        submitBtn.grid(row=2, column=1, padx=5, pady=10)

    def createTreeView(self):
        self.columns = ("Teacher_Code", "Teacher_Name", "Birthday", "Gender", "Department", "Email", "Phone", "Address")
        self.tree = Treeview(self, columns=self.columns, show="headings")

        self.tree.column("Teacher_Code", width=100)
        self.tree.heading("Teacher_Code", text="Mã giáo viên")

        self.tree.column("Teacher_Name", width=150)
        self.tree.heading("Teacher_Name", text="Tên giáo viên")

        self.tree.column("Birthday", width=100)
        self.tree.heading("Birthday", text="Ngày sinh")

        self.tree.column("Gender", width=80)
        self.tree.heading("Gender", text="Giới tính")

        self.tree.column("Department", width=150)
        self.tree.heading("Department", text="Khoa/ Phòng ban")

        self.tree.column("Email", width=150)
        self.tree.heading("Email", text="Email")

        self.tree.column("Phone", width=100)
        self.tree.heading("Phone", text="Số điện thoại")

        self.tree.column("Address", width=200)
        self.tree.heading("Address", text="Địa chỉ")

        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<Double-1>", self.editTeacher)
        self.tree.bind("<Delete>", self.handleDelete)

    def initData(self):
        response = teacherAPI.getAllTeachers()
        if "success" in response and response["success"]:
            teachers = response["data"]
            for teacher in teachers:
                self.insertItemToTree(teacher)

    def insertItemToTree(self, teacher):
        self.tree.insert("", "end", text=teacher["id"],
                         values=(teacher["teacherCode"], teacher["name"], teacher["dob"], teacher["gender"],
                                 teacher["major"]["majorName"] if teacher["major"] else "", teacher["email"], teacher["phone"], teacher["address"]))

    def handleCreateTeacher(self):
        data = {
            "teacherCode": self.teacherCode.get(),
            "name": self.name.get(),
            "email": self.email.get(),
            "phone": self.phone.get(),
            "address": self.address.get(),
            "dob": self.dob.get(),
            "gender": self.gender.get(),
            "major": self.majorsList[self.major.current()],
            "password": self.dob.get().replace("-", "")
        }

        response = teacherAPI.createTeacher(data)
        if response["success"]:
            self.insertItemToTree(response["data"][0])
            messagebox.showinfo("Success", "Thêm giáo viên thành công. Mật khẩu mặc định là ngày sinh của giáo viên (yyyymmdd)")
            self.clearForm()
        else:
            messagebox.showerror("Error", response["message"])

    def clearForm(self):
        self.teacherCode.delete(0, END)
        self.name.delete(0, END)
        self.email.delete(0, END)
        self.phone.delete(0, END)
        self.address.delete(0, END)
        self.dob.config(state="normal")
        self.dob.delete(0, END)
        self.dob.config(state="readonly")
        self.gender.set("")
        self.major.set("")

    def editTeacher(self, event):
        selected = event.widget.selection()[0]
        teacherId = event.widget.item(selected)["text"]
        teacherData = event.widget.item(selected)["values"]

        root = Toplevel(self)
        root.title("Chỉnh sửa thông tin giáo viên")

        formController = Frame(root)
        formController.pack(padx=10, pady=10)

        Label(formController, text="Mã giáo viên").grid(row=0, column=0)
        code = Entry(formController)
        code.insert(0, teacherData[0])
        code.grid(row=0, column=1, padx=5, pady=10)

        Label(formController, text="Tên giáo viên").grid(row=1, column=0)
        name = Entry(formController)
        name.insert(0, teacherData[1])
        name.grid(row=1, column=1, padx=5, pady=10)

        Label(formController, text="Ngày sinh").grid(row=2, column=0)
        dobEntry = Entry(formController)
        dobEntry.insert(0, teacherData[2])
        dobEntry.config(state="readonly")
        dobEntry.grid(row=2, column=1, padx=5, pady=10)

        dobBtn = Button(formController, text="Chọn ngày", command=lambda: self.openCalendar(dobEntry, teacherData[2]))
        dobBtn.grid(row=2, column=2, padx=5, pady=10)

        Label(formController, text="Giới tính").grid(row=3, column=0)
        genderEntry = Combobox(formController, values=["Male", "Female"])
        genderEntry.insert(0, teacherData[3])
        genderEntry.grid(row=3, column=1, padx=5, pady=10)

        Label(formController, text="Khoa/ Phòng ban").grid(row=4, column=0)
        departmentEntry = Combobox(formController, values=[major["majorName"] for major in self.majorsList])
        departmentEntry.insert(0, teacherData[4])
        departmentEntry.grid(row=4, column=1, padx=5, pady=10)

        Label(formController, text="Email").grid(row=5, column=0)
        email = Entry(formController)
        email.insert(0, teacherData[5])
        email.grid(row=5, column=1, padx=5, pady=10)

        Label(formController, text="Số điện thoại").grid(row=6, column=0)
        phone = Entry(formController)
        phone.insert(0, teacherData[6])
        phone.grid(row=6, column=1, padx=5, pady=10)

        Label(formController, text="Địa chỉ").grid(row=7, column=0)
        address = Entry(formController)
        address.insert(0, teacherData[7])
        address.grid(row=7, column=1, padx=5, pady=10)

        submitBtn = Button(formController, text="Cập nhật thông tin", command=lambda: self.updateTeacher({
            "teacherId": teacherId,
            "teacherCode": code.get(),
            "name": name.get(),
            "dob": dobEntry.get(),
            "gender": genderEntry.get(),
            "major": self.majorsList[departmentEntry.current()],
            "email": email.get(),
            "phone": phone.get(),
            "address": address.get()
        }, root))
        submitBtn.grid(row=8, column=1, padx=5, pady=10)

    def handleDelete(self, event):
        selected = event.widget.selection()[0]
        teacherId = event.widget.item(selected)["text"]

        response = messagebox.askyesno("Delete", "Are you sure you want to delete this teacher?")
        if response:
            response = teacherAPI.deleteTeacher(teacherId)
            if response["success"]:
                self.tree.delete(selected)
            else:
                messagebox.showerror("Error", response["message"])

    def updateTeacher(self, data, root):
        response = teacherAPI.updateTeacher(data)
        if response["success"]:
            for item in self.tree.get_children():
                if self.tree.item(item)["text"] == data["teacherId"]:
                    self.tree.item(item, values=(data["teacherCode"], data["name"], data["dob"], data["gender"], data["major"]["majorName"], data["email"], data["phone"], data["address"]))
            messagebox.showinfo("Success", "Cập nhật thông tin giáo viên thành công")
            root.destroy()
        else:
            messagebox.showerror("Error", response["message"])

    def openCalendar(self, dobEntry, birthDate):
        birthYear, birthMonth, birthDay = birthDate.split("-") if birthDate != None else (2000, 1, 1)

        top = Toplevel(self)
        cal = Calendar(top, selectmode="day", year=int(birthYear), month=int(birthMonth), day=int(birthDay))
        cal.pack(padx=10, pady=10)

        def grab_date():
            date = cal.selection_get()
            formatted_date = date.strftime('%Y-%m-%d')
            dobEntry.config(state="normal")
            dobEntry.delete(0, END)
            dobEntry.insert(0, formatted_date)
            dobEntry.config(state="readonly")
            top.destroy()

        Button(top, text="Chọn", command=grab_date).pack(pady=10)