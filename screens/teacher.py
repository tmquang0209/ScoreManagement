from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkcalendar import Calendar

from API import major

from API import teacher

class Teacher(Frame):
    def __init__ (self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.initUI()
        self.initData()

    def initUI(self):
        title = Label(self, text="Danh sách giáo viên", font=("Helvetica", 18))
        title.pack(side="top", fill="x", pady=10, padx=10)

        # Tree
        self.tree = Treeview(self, columns=("Code", "Name", "Birthday", "Gender", "Department", "Email", "Phone", "Address"), show="headings", padding=10)

        self.tree.column("Code", width=100)
        self.tree.heading("Code", text="Mã giáo viên")

        self.tree.heading("Name", text="Tên giáo viên")

        self.tree.column("Birthday", width=100)
        self.tree.heading("Birthday", text="Ngày sinh")

        self.tree.column("Gender", width=100)
        self.tree.heading("Gender", text="Giới tính")

        self.tree.heading("Department", text="Khoa/ Phòng ban")

        self.tree.column("Email", width=100)
        self.tree.heading("Email", text="Email")

        self.tree.column("Phone", width=100)
        self.tree.heading("Phone", text="Số điện thoại")

        self.tree.heading("Address", text="Địa chỉ")
        self.tree.pack()

        self.tree.bind("<Double-1>", self.editTeacher)
        self.tree.bind("<Delete>", self.handleDelete)

    def initData(self):
        # remove all items in tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        response = teacher.getAllTeachers()

        if "success" in response and response["success"]:
            for item in response["data"]:
                self.insertItemToTree(item)

    def handleUpdateTeacherTree(self, id, data):
        for selectedItem in self.tree.selection():
            self.tree.item(selectedItem, text=id, values=(data["teacherCode"], data["name"], data["dob"], data["gender"], data["major"]["majorName"] if data["major"] != None else "", data["email"], data["phone"], data["address"]))

    def insertItemToTree(self, teacher):
        self.tree.insert("", "end", text=teacher["id"], values=(teacher["teacherCode"], teacher["name"], teacher["dob"], teacher["gender"], teacher["major"]["majorName"] if teacher["major"] != None else "", teacher["email"], teacher["phone"], teacher["address"]))

    def handleEditTeacher(self, root, id, data):
        response = teacher.updateTeacher(id, data)
        if response["success"]:
            self.handleUpdateTeacherTree(id, data)
            messagebox.showinfo("Success", "Cập nhật giáo viên thành công")
            root.destroy()
        else:
            messagebox.showerror("Error", response["message"])

    def editTeacher(self, event):
        item = event.widget.selection()[0]
        id = event.widget.item(item, "text")
        data = event.widget.item(item, "values")

        # get major list
        majorsList = major.getAllMajors()["data"]

        root = Toplevel(self)
        root.title("Cập nhật thông tin giáo viên")

        formController = Frame(root)
        formController.pack(padx=10, pady=10)

        Label(formController, text="Mã giáo viên").grid(row=0, column=0)
        code = Entry(formController, width=25)
        code.grid(row=0, column=1, padx=5, pady=10)
        code.insert(0, data[0])

        Label(formController, text="Tên giáo viên").grid(row=1, column=0)
        name = Entry(formController, width=25)
        name.grid(row=1, column=1, padx=5, pady=10)
        name.insert(0, data[1])

        Label(formController, text="Ngày sinh").grid(row=2, column=0)
        dobEntry = Entry(formController, width=25)
        dobEntry.grid(row=2, column=1, padx=10, pady=5)
        dobEntry.insert(0, data[2] if data[2] != None else "")
        dobEntry.config(state="readonly")

        # choose date button
        chooseDateButton = Button(formController, text="Chọn ngày", command=lambda: self.openCalendar(dobEntry, data[2]))
        chooseDateButton.grid(row=2, column=2, padx=10, pady=5)

        Label(formController, text="Giới tính").grid(row=3, column=0)
        genderEntry = Combobox(formController, values=["Male", "Female"], width=25)
        genderEntry.insert(0, data[3])
        genderEntry.grid(row=3, column=1, padx=10, pady=5)

        Label(formController, text="Khoa/ Phòng ban").grid(row=4, column=0)
        departmentEntry = Combobox(formController, values=[major["majorName"] for major in majorsList], width=25)
        departmentEntry.insert(0, data[4])
        departmentEntry.grid(row=4, column=1, padx=10, pady=5)

        Label(formController, text="Email").grid(row=5, column=0)
        email = Entry(formController, width=25)
        email.grid(row=5, column=1, padx=5, pady=10)
        email.insert(0, data[5])

        Label(formController, text="Số điện thoại").grid(row=6, column=0)
        phone = Entry(formController, width=25)
        phone.grid(row=6, column=1, padx=5, pady=10)
        phone.insert(0, data[6])

        Label(formController, text="Địa chỉ").grid(row=7, column=0)
        address = Entry(formController, width=25)
        address.grid(row=7, column=1, padx=5, pady=10)
        address.insert(0, data[7])

        submitButton = Button(formController, text="Cập nhật", command=lambda: self.handleEditTeacher(root, id, {
            "teacherCode": code.get(),
            "name": name.get(),
            "dob": dobEntry.get(),
            "gender": genderEntry.get(),
            "major": majorsList[departmentEntry.current()],
            "email": email.get(),
            "phone": phone.get(),
            "address": address.get()
        }))
        submitButton.grid(row=8, column=1, padx=5, pady=10)

    def openCalendar(self, dobEntry, birthDate):
        birthYear, birthMonth, birthDay = birthDate.split("-") if birthDate != "" else (2000, 1, 1)

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


    def handleDelete(self, event):
        item = event.widget.selection()[0]
        data = event.widget.item(item, "values")

        confirmation = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa giáo viên này?")
        if not confirmation:
            return

        response = teacher.deleteTeacher(data[0])
        if response["success"]:
            self.tree.delete(item)
            messagebox.showinfo("Success", "Xóa giáo viên thành công")
        else:
            messagebox.showerror("Error", response["message"])

class TeacherCreate(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.initUI()

    def initUI(self):
        # get major list
        majorsList = major.getAllMajors()["data"]

        title = Label(self, text="Thêm giáo viên mới", font=("Helvetica", 18))
        title.pack(side="top", fill="x", pady=10, padx=10)

        form = Frame(self)
        form.pack(padx=10, pady=10)

        Label(form, text="Mã giáo viên").grid(row=0, column=0)
        code = Entry(form)
        code.grid(row=0, column=1, padx=5, pady=10)

        Label(form, text="Tên giáo viên").grid(row=1, column=0)
        name = Entry(form)
        name.grid(row=1, column=1, padx=5, pady=10)

        Label(form, text="Email").grid(row=2, column=0)
        email = Entry(form)
        email.grid(row=2, column=1, padx=5, pady=10)

        Label(form, text="Số điện thoại").grid(row=3, column=0)
        phone = Entry(form)
        phone.grid(row=3, column=1, padx=5, pady=10)

        Label(form, text="Địa chỉ").grid(row=4, column=0)
        address = Entry(form)
        address.grid(row=4, column=1, padx=5, pady=10)

        Label(form, text="Ngày sinh").grid(row=5, column=0)
        dobEntry = Entry(form)
        dobEntry.grid(row=5, column=1, padx=10, pady=5)
        dobEntry.config(state="readonly")

        # choose date button
        chooseDateButton = Button(form, text="Chọn ngày", command=lambda: self.openCalendar(dobEntry))
        chooseDateButton.grid(row=5, column=2, padx=10, pady=5)

        Label(form, text="Giới tính").grid(row=6, column=0)
        genderEntry = Combobox(form, values=["Male","Female"])
        genderEntry.grid(row=6, column=1, padx=10, pady=5)

        Label(form, text="Khoa/ Phòng ban").grid(row=7, column=0)
        departmentEntry = Combobox(form, values=[major["majorName"] for major in majorsList])
        departmentEntry.grid(row=7, column=1, padx=10, pady=5)

        submitButton = Button(form, text="Thêm giáo viên", command=lambda: self.handleSubmit({
            "teacherCode": code.get(),
            "name": name.get(),
            "email": email.get(),
            "phone": phone.get(),
            "address": address.get(),
            "dob": dobEntry.get(),
            "major": majorsList[departmentEntry.current()],
            "password": dobEntry.get().replace("-", "")
        }))
        submitButton.grid(row=8, column=1, padx=5, pady=10)

    def handleSubmit(self, data):
        response = teacher.createTeacher(data)
        if response["success"]:
            self.controller.screens["Teacher"].insertItemToTree(response["data"][0])
            messagebox.showinfo("Success", "Thêm giáo viên thành công. Mật khẩu mặc định là ngày sinh của giáo viên (yyyymmdd)")
        else:
            messagebox.showerror("Error", response["message"])

    def openCalendar(self, dobEntry):
        birthYear, birthMonth, birthDay = (2000, 1, 1)

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
