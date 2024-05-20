from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

from tkcalendar import Calendar

from API import employee as employeeAPI, department as departmentAPI, role as roleAPI

from API import employee

class Employee(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.initUI()

    def initUI(self):
        self.tree = Treeview(self, columns=("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9"), show="headings")

        self.tree.column("#1", width=70)
        self.tree.heading("#1", text="Mã NV")

        self.tree.heading("#2", text="Tên NV")

        self.tree.column("#3", width=100)
        self.tree.heading("#3", text="SĐT")

        self.tree.column("#4", width=100)
        self.tree.heading("#4", text="Email")

        self.tree.heading("#5", text="Địa chỉ")

        self.tree.column("#6", width=80)
        self.tree.heading("#6", text="Ngày sinh")

        self.tree.column("#7", width=60)
        self.tree.heading("#7", text="Giới tính")

        self.tree.column("#8", width=100)
        self.tree.heading("#8", text="Chức vụ")

        self.tree.heading("#9", text="Phòng ban")

        self.tree.bind("<Double-1>", self.editEmployee)

        self.tree.pack(pady=20)
        self.tree.xview_moveto(0.5)

    def insertToTree(self, item):
        self.tree.insert("", "end",text=item["id"], values=(item["code"], item["name"], item["phone"], item["email"], item["address"], item["dob"], item["gender"], item["role"]["name"] if item["role"] else "", item["department"]["name"] if "department" in item and item["department"] != None else ""))

    def updateEmployeeInTree(self, item):
        selected = self.tree.selection()[0]
        self.tree.insert("", "end",text=item["id"], values=(item["code"], item["name"], item["phone"], item["email"], item["address"], item["dob"], item["gender"], item["role"]["name"] if item["role"] else "", item["department"]["name"] if "department" in item and item["department"] != None else ""))
    def initData(self):
        self.tree.delete(*self.tree.get_children())

        response = employee.getAllEmployees()
        if response["success"]:
            data = response["data"]
            for item in data:
                self.insertToTree(item)

    def editEmployee(self, event):
        def handleUpdateEmployee(id, code, name, phone, email, address, dob, gender, role, department):
            response = employeeAPI.updateEmployee(id, {
                "code": code,
                "name": name,
                "phone": phone,
                "email": email,
                "address": address,
                "dob": dob,
                "gender": gender,
                "role": role,
                "department": department
            })

            if response["success"]:
                self.updateEmployeeInTree(response["data"][0])
                messagebox.showinfo("Success", "Employee updated successfully")
                root.destroy()
            else:
                messagebox.showerror("Error", response["message"])

        roles_response = roleAPI.getAllRoles()
        roles = roles_response["data"] if roles_response["success"] else []
        departments_response = departmentAPI.getDepartments()
        departments = departments_response["data"] if departments_response["success"] else []

        item = event.widget.selection()[0]
        id = event.widget.item(item, "text")
        data = event.widget.item(item, "values")

        root = Toplevel(self)
        root.title("Chỉnh sửa thông tin nhân viên")

        formController = Frame(root)
        formController.pack()

        Label(formController, text="Mã nhân viên").grid(row=0, column=0, padx=5, pady=10)
        code = Entry(formController)
        code.grid(row=0, column=1, padx=5, pady=10)
        code.insert(0, data[0])

        Label(formController, text="Tên nhân viên").grid(row=1, column=0, padx=5, pady=10)
        name = Entry(formController)
        name.grid(row=1, column=1, padx=5, pady=10)
        name.insert(0, data[1])

        Label(formController, text="Số điện thoại").grid(row=2, column=0, padx=5, pady=10)
        phone = Entry(formController)
        phone.grid(row=2, column=1, padx=5, pady=10)
        phone.insert(0, data[2])

        Label(formController, text="Email").grid(row=3, column=0, padx=5, pady=10)
        email = Entry(formController)
        email.grid(row=3, column=1, padx=5, pady=10)
        email.insert(0, data[3])

        Label(formController, text="Địa chỉ").grid(row=4, column=0, padx=5, pady=10)
        address = Entry(formController)
        address.grid(row=4, column=1, padx=5, pady=10)
        address.insert(0, data[4])

        Label(formController, text="Ngày sinh").grid(row=5, column=0, padx=5, pady=10)
        dob = Entry(formController)
        dob.grid(row=5, column=1, padx=5, pady=10)
        dob.insert(0, data[5])
        dob.config(state="readonly")

        # Open calendar to select date
        Button(formController, text="Chọn ngày", command=lambda: self.openCalendar(dob, data[5])).grid(row=5, column=2, padx=5, pady=10)

        Label(formController, text="Giới tính").grid(row=6, column=0, padx=5, pady=10)
        gender = Combobox(formController, values=["Male", "Female"])
        gender.grid(row=6, column=1, padx=5, pady=10)
        gender.insert(0, data[6])

        Label(formController, text="Chức vụ").grid(row=7, column=0, padx=5, pady=10)
        role = Combobox(formController, values=[role["name"] for role in roles])
        role.grid(row=7, column=1, padx=5, pady=10)
        role.insert(0, data[7])

        Label(formController, text="Phòng ban").grid(row=8, column=0, padx=5, pady=10)
        department = Combobox(formController, values=[department["name"] for department in departments])
        department.grid(row=8, column=1, padx=5, pady=10)

        # Set the initial value for department if available
        department_index = next((index for (index, d) in enumerate(departments) if d["name"] == data[8]), -1)
        if department_index != -1:
            department.current(department_index)

        Button(formController, text="Lưu", command=lambda: handleUpdateEmployee(
            id, code.get(), name.get(), phone.get(), email.get(), address.get(), dob.get(), gender.get(),
            roles[role.current()], departments[department.current()]
        )).grid(row=9, column=1, padx=5, pady=10)

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

class EmployeeCreate(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.initUI()

    def initUI(self):
        formController = Frame(self)
        formController.pack()

        Label(formController, text="Mã nhân viên").grid(row=0, column=0, padx=5, pady=10)
        self.code = Entry(formController)
        self.code.grid(row=0, column=1, padx=5, pady=10)

        Label(formController, text="Tên nhân viên").grid(row=1, column=0, padx=5, pady=10)
        self.name = Entry(formController)
        self.name.grid(row=1, column=1, padx=5, pady=10)

        Label(formController, text="Số điện thoại").grid(row=2, column=0, padx=5, pady=10)
        self.phone = Entry(formController)
        self.phone.grid(row=2, column=1, padx=5, pady=10)

        Label(formController, text="Email").grid(row=3, column=0, padx=5, pady=10)
        self.email = Entry(formController)
        self.email.grid(row=3, column=1, padx=5, pady=10)

        Label(formController, text="Địa chỉ").grid(row=4, column=0, padx=5, pady=10)
        self.address = Entry(formController)
        self.address.grid(row=4, column=1, padx=5, pady=10)

        Label(formController, text="Ngày sinh").grid(row=5, column=0, padx=5, pady=10)
        self.dob = Entry(formController, state="readonly")
        self.dob.grid(row=5, column=1, padx=5, pady=10)

        # Open calendar to select date
        Button(formController, text="Chọn ngày", command=lambda: self.openCalendar(self.dob)).grid(row=5, column=2, padx=5, pady=10)

        Label(formController, text="Giới tính").grid(row=6, column=0, padx=5, pady=10)
        self.gender = Combobox(formController, values=["Male", "Female"])
        self.gender.grid(row=6, column=1, padx=5, pady=10)

        roles_response = roleAPI.getAllRoles()
        roles = roles_response["data"] if roles_response["success"] else []
        departments_response = departmentAPI.getDepartments()
        departments = departments_response["data"] if "success" in departments_response and departments_response["success"] else []

        Label(formController, text="Chức vụ").grid(row=7, column=0, padx=5, pady=10)
        self.role = Combobox(formController, values=[role["name"] for role in roles])
        self.role.grid(row=7, column=1, padx=5, pady=10)

        Label(formController, text="Phòng ban").grid(row=8, column=0, padx=5, pady=10)
        self.department = Combobox(formController, values=[department["name"] for department in departments])
        self.department.grid(row=8, column=1, padx=5, pady=10)

        Button(formController, text="Lưu", command=lambda:self.createEmployee(
            self.code.get(),
            self.name.get(),
            self.phone.get(),
            self.email.get(),
            self.address.get(),
            self.dob.get(),
            self.gender.get(),
            roles[self.role.current()],
            departments[self.department.current()]
        )).grid(row=9, column=1, padx=5, pady=10)

    def createEmployee(self, code, name, phone, email, address, dob, gender, role, department):
        response = employeeAPI.createEmployee({
            "code": code,
            "name": name,
            "phone": phone,
            "email": email,
            "address": address,
            "password": dob.replace("-", ""),
            "dob": dob,
            "gender": gender,
            "role": role,
            "department": department
        })

        if response["success"]:
            self.controller.screens["Employee"].initData()
            messagebox.showinfo("Success", "Employee created successfully")
            self.controller.showFrame("Employee")
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