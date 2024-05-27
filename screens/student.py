from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkcalendar import Calendar

from API import student as studentAPI, major as majorAPI

class Student(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.initUI()

    def initUI(self):
        title = Label(self, text="Danh sách sinh viên", font=("Helvetica", 18))
        title.pack(side="top", fill="x", pady=10, padx=10)

        self.columns = ("Student_Code", "Student_Name", "Email", "Phone", "Address", "Dob", "Gender", "Major")
        self.tree = Treeview(self, columns=self.columns, show="headings")

        self.tree.column("Student_Code", width=50)
        self.tree.heading("Student_Code", text="Mã SV")

        self.tree.column("Student_Name", width=100)
        self.tree.heading("Student_Name", text="Họ tên")

        self.tree.column("Email", width=125)
        self.tree.heading("Email", text="Email")

        self.tree.column("Phone", width=100)
        self.tree.heading("Phone", text="Phone")

        self.tree.column("Address", width=100)
        self.tree.heading("Address", text="Địa chỉ")

        self.tree.column("Dob", width=50)
        self.tree.heading("Dob", text="Dob")

        self.tree.column("Gender", width=80)
        self.tree.heading("Gender", text="Giới tính")

        self.tree.heading("Major", text="Ngành")

        self.tree.pack()

        self.tree.bind("<Double-1>", self.editStudent)
        self.tree.bind("<Delete>", self.deleteStudent)

    def handleInsertStudentTree(self, student):
        self.tree.insert("", "end",
                         text=student["id"],
                         values=(student["studentCode"], student["name"],
                                 student["email"], student["phone"],
                                 student["address"], student["dob"],
                                 student["gender"],
                                 student["major"]["majorName"] if student["major"] else ""))

    def handleUpdateStudentTree(self, student):
        selected = self.tree.selection()[0]
        self.tree.item(selected,
                       text=student["id"],
                       values=(student["studentCode"], student["name"],
                               student["email"], student["phone"],
                               student["address"], student["dob"],
                               student["gender"],
                               student["major"]["majorName"] if student["major"] else ""))

    def initData(self):
        response = studentAPI.getAllStudents()

        if response["success"]:
            students = response["data"]
            for student in students:
                self.handleInsertStudentTree(student)

    def handleEditStudent(self, root, id, studentCode, name, email, phone, address, dob, gender, major):
        response = studentAPI.updateStudent(id, {
            "studentCode": studentCode,
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "dob": dob,
            "gender": gender,
            "major": major
        })

        if response["success"]:
            self.handleUpdateStudentTree(response["data"][0])
            messagebox.showinfo("Thành công", "Cập nhật thông tin sinh viên thành công")
            root.destroy()
        else:
            messagebox.showerror("Lỗi", response["message"])

    def editStudent(self, event):
        majorsList = majorAPI.getAllMajors()["data"] if majorAPI.getAllMajors()["success"] else []

        root = Toplevel(self)
        root.title("Chỉnh sửa thông tin sinh viên")

        selected = event.widget.selection()[0]
        studentId = event.widget.item(selected)["text"]
        studentData = event.widget.item(selected)["values"]

        formController = Frame(root)
        formController.pack(padx=10, pady=10)

        Label(formController, text="Mã sinh viên").grid(row=0, column=0)
        studentCode = Entry(formController)
        studentCode.insert(0, studentData[0])
        studentCode.grid(row=0, column=1, padx=5, pady=10)

        Label(formController, text="Họ tên").grid(row=1, column=0)
        name = Entry(formController)
        name.insert(0, studentData[1])
        name.grid(row=1, column=1, padx=5, pady=10)

        Label(formController, text="Email").grid(row=2, column=0)
        email = Entry(formController)
        email.insert(0, studentData[2])
        email.grid(row=2, column=1, padx=5, pady=10)

        Label(formController, text="Phone").grid(row=3, column=0)
        phone = Entry(formController)
        phone.insert(0, studentData[3])
        phone.grid(row=3, column=1, padx=5, pady=10)

        Label(formController, text="Địa chỉ").grid(row=4, column=0)
        address = Entry(formController)
        address.insert(0, studentData[4])
        address.grid(row=4, column=1, padx=5, pady=10)

        Label(formController, text="Ngày sinh").grid(row=5, column=0)
        dob = Entry(formController)
        dob.insert(0, studentData[5])
        dob.config(state="readonly")
        dob.grid(row=5, column=1, padx=5, pady=10)

        # Open calendar
        dobBtn = Button(formController, text="Chọn ngày", command=lambda: self.openCalendar(dob, studentData[5]))
        dobBtn.grid(row=5, column=2, padx=5, pady=10)

        Label(formController, text="Giới tính").grid(row=6, column=0)
        gender = Combobox(formController, values=["Male", "Female"])
        gender.insert(0, studentData[6])
        gender.grid(row=6, column=1, padx=5, pady=10)

        Label(formController, text="Ngành").grid(row=7, column=0)
        major = Combobox(formController, values=[major["majorName"] for major in majorsList])
        major.insert(0, studentData[7])
        major.grid(row=7, column=1, padx=5, pady=10)

        submitBtn = Button(formController, text="Cập nhật", command=lambda: self.handleEditStudent(root,
                                                                                                   studentId,
                                                                                                   studentCode.get(),
                                                                                                   name.get(),
                                                                                                   email.get(),
                                                                                                   phone.get(),
                                                                                                   address.get(),
                                                                                                   dob.get(),
                                                                                                   gender.get(),
                                                                                                    majorsList[major.current()]))
        submitBtn.grid(row=8, column=1, padx=5, pady=10)

    def openCalendar(self, dobEntry, birthDate):
        birthYear, birthMonth, birthDay = birthDate.split("-") if birthDate != "None" else (2000, 1, 1)

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

    def deleteStudent(self, event):
        confirmation = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa sinh viên này không?")
        if confirmation:
            selected = event.widget.selection()[0]
            studentId = event.widget.item(selected)["text"]

            response = studentAPI.deleteStudent(studentId)

            if response["success"]:
                self.tree.delete(selected)
                messagebox.showinfo("Thành công", "Xóa sinh viên thành công")
            else:
                messagebox.showerror("Lỗi", response["message"])

class StudentCreate(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.initUI()

    def initUI(self):
        majorsList = majorAPI.getAllMajors()["data"] if majorAPI.getAllMajors()["success"] else []

        title = Label(self, text="Thêm sinh viên mới", font=("Helvetica", 18))
        title.pack(side="top", fill="x", pady=10, padx=10)

        formController = Frame(self)
        formController.pack(padx=10, pady=10)

        Label(formController, text="Mã sinh viên").grid(row=0, column=0)
        studentCode = Entry(formController)
        studentCode.grid(row=0, column=1, padx=5, pady=10)

        Label(formController, text="Họ tên").grid(row=1, column=0)
        name = Entry(formController)
        name.grid(row=1, column=1, padx=5, pady=10)

        Label(formController, text="Email").grid(row=2, column=0)
        email = Entry(formController)
        email.grid(row=2, column=1, padx=5, pady=10)

        Label(formController, text="Phone").grid(row=3, column=0)
        phone = Entry(formController)
        phone.grid(row=3, column=1, padx=5, pady=10)

        Label(formController, text="Địa chỉ").grid(row=4, column=0)
        address = Entry(formController)
        address.grid(row=4, column=1, padx=5, pady=10)

        Label(formController, text="Ngày sinh").grid(row=5, column=0)
        dob = Entry(formController)
        dob.config(state="readonly")
        dob.grid(row=5, column=1, padx=5, pady=10)

        # Open calendar
        dobBtn = Button(formController, text="Chọn ngày", command=lambda: self.openCalendar(dob, dob.get() if dob.get() != "" else "None"))
        dobBtn.grid(row=5, column=2, padx=5, pady=10)

        Label(formController, text="Giới tính").grid(row=6, column=0, padx=5, pady=10)
        gender = Combobox(formController, values=["Male", "Female"])
        gender.grid(row=6, column=1, padx=5, pady=10)

        Label(formController, text="Ngành").grid(row=7, column=0)
        major = Combobox(formController, values=[major["majorName"] for major in majorsList])
        major.grid(row=7, column=1, padx=5, pady=10)

        submitBtn = Button(formController, text="Thêm sinh viên",
                           command=lambda: self.handleCreateStudent(studentCode.get(), name.get(),
                                                                    email.get(), phone.get(),
                                                                    address.get(), dob.get(),
                                                                    gender.get(), majorsList[major.current()]))
        submitBtn.grid(row=8, column=1, padx=5, pady=10)

    def handleCreateStudent(self, studentCode, name, email, phone, address, dob, gender, major):
        response = studentAPI.createStudent({
            "studentCode": studentCode,
            "password": dob.replace("-", ""),
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "dob": dob,
            "gender": gender,
            "major": major
        })

        if response["success"]:
            self.controller.screens["Student"].handleInsertStudentTree(response["data"][0])
            messagebox.showinfo("Thành công", "Thêm sinh viên mới thành công, mật khẩu mặc định (yyyymmdd)")
            self.controller.showFrame("Student")

        else:
            messagebox.showerror("Lỗi", response["message"])

    def openCalendar(self, dobEntry, birthDate):
        birthYear, birthMonth, birthDay = birthDate.split("-") if birthDate != "None" else (2000, 1, 1)

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