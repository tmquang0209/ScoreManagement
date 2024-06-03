from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkcalendar import Calendar
from API import employee as employeeAPI, department as departmentAPI, role as roleAPI
class Employee(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.initUI()

    def initUI(self):
        self.formController = Frame(self)
        self.formController.pack()

        self.createForm(self.formController)

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
        self.tree.bind("<Delete>", self.deleteEmployee)

        self.tree.pack(pady=20)

    def deleteEmployee(self, event):
        selected = self.tree.selection()[0]
        id = self.tree.item(selected, "text")

        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa nhân viên này?"):
            response = employeeAPI.deleteEmployee(id)
            if response["success"]:
                self.tree.delete(selected)
            else:
                messagebox.showerror("Lỗi", response["message"])

    def createForm(self, parent):
        Label(parent, text="Mã nhân viên").grid(row=0, column=0, padx=5, pady=10)
        self.code = Entry(parent)
        self.code.grid(row=0, column=1, padx=5, pady=10)

        Label(parent, text="Tên nhân viên").grid(row=0, column=3, padx=5, pady=10)
        self.name = Entry(parent)
        self.name.grid(row=0, column=4, padx=5, pady=10)

        Label(parent, text="Số điện thoại").grid(row=0, column=5, padx=5, pady=10)
        self.phone = Entry(parent)
        self.phone.grid(row=0, column=6, padx=5, pady=10)

        Label(parent, text="Email").grid(row=0, column=7, padx=5, pady=10)
        self.email = Entry(parent)
        self.email.grid(row=0, column=8, padx=7, pady=10)

        Label(parent, text="Địa chỉ").grid(row=2, column=0, padx=5, pady=10)
        self.address = Entry(parent)
        self.address.grid(row=2, column=1, padx=5, pady=10)

        Label(parent, text="Ngày sinh").grid(row=1, column=0, padx=5, pady=10)
        self.dob = Entry(parent, state="readonly")
        self.dob.grid(row=1, column=1, padx=5, pady=10)

        Button(parent, text="Chọn ngày", command=lambda: self.openCalendar(self.dob)).grid(row=1, column=2, padx=5, pady=10)

        Label(parent, text="Giới tính").grid(row=1, column=3, padx=5, pady=10)
        self.gender = Combobox(parent, values=["Male", "Female"])
        self.gender.grid(row=1, column=4, padx=5, pady=10)

        roles_response = roleAPI.getAllRoles()
        self.roles = roles_response["data"] if "success" in roles_response and roles_response["success"] else []
        departments_response = departmentAPI.getDepartments()
        self.departments = departments_response["data"] if "success" in departments_response and departments_response["success"] else []

        Label(parent, text="Chức vụ").grid(row=1, column=5, padx=5, pady=10)
        self.role = Combobox(parent, values=[role["name"] for role in self.roles])
        self.role.grid(row=1, column=6, padx=5, pady=10)

        Label(parent, text="Phòng ban").grid(row=1, column=7, padx=5, pady=10)
        self.department = Combobox(parent, values=[department["name"] for department in self.departments])
        self.department.grid(row=1, column=8, padx=5, pady=10)

        self.save_button = Button(parent, text="Tạo mới", command=self.handleSaveEmployee)
        self.save_button.grid(row=3, column=0, padx=5, pady=10)

        self.cancelButton = Button(parent, text="Hủy", command=self.clearForm)
        self.cancelButton.grid(row=3, column=1, padx=5, pady=10)

    def insertToTree(self, item):
        self.tree.insert("", "end",
                         text=item["id"],
                         values=(item["code"], item["name"],
                                 item["phone"], item["email"],
                                 item["address"], item["dob"],
                                 item["gender"],
                                 item["role"]["name"] if item["role"] else "", item["department"]["name"] if "department" in item and item["department"] is not None else ""))

    def updateEmployeeInTree(self, item):
        selected = self.tree.selection()[0]
        self.tree.item(selected,
                       text=item["id"],
                       values=(item["code"], item["name"],
                               item["phone"], item["email"],
                               item["address"], item["dob"],
                               item["gender"],
                               item["role"]["name"] if item["role"] else "", item["department"]["name"] if "department" in item and item["department"] is not None else ""))

    def initData(self):
        self.tree.delete(*self.tree.get_children())
        response = employeeAPI.getAllEmployees()

        if "success" in response and response["success"]:
            data = response["data"]
            for item in data:
                self.insertToTree(item)

    def editEmployee(self, event):
        item = self.tree.selection()[0]
        id = self.tree.item(item, "text")
        data = self.tree.item(item, "values")

        self.code.delete(0, END)
        self.code.insert(0, data[0])
        self.name.delete(0, END)
        self.name.insert(0, data[1])
        self.phone.delete(0, END)
        self.phone.insert(0, data[2])
        self.email.delete(0, END)
        self.email.insert(0, data[3])
        self.address.delete(0, END)
        self.address.insert(0, data[4])
        self.dob.config(state="normal")
        self.dob.delete(0, END)
        self.dob.insert(0, data[5])
        self.dob.config(state="readonly")
        self.gender.set(data[6])

        role_index = next((index for (index, role) in enumerate(self.roles) if role["name"] == data[7]), -1)
        if role_index != -1:
            self.role.current(role_index)

        department_index = next((index for (index, department) in enumerate(self.departments) if department["name"] == data[8]), -1)
        if department_index != -1:
            self.department.current(department_index)

        self.save_button.config(text="Cập nhật", command=lambda: self.handleUpdateEmployee(id))

    def clearForm(self):
        self.code.delete(0, END)
        self.name.delete(0, END)
        self.phone.delete(0, END)
        self.email.delete(0, END)
        self.address.delete(0, END)
        self.dob.config(state="normal")
        self.dob.delete(0, END)
        self.dob.config(state="readonly")
        self.gender.set("")
        self.role.set("")
        self.department.set("")

        self.save_button.config(text="Tạo mới",command=self.handleSaveEmployee)

    def handleSaveEmployee(self):
        response = employeeAPI.createEmployee({
            "code": self.code.get(),
            "name": self.name.get(),
            "phone": self.phone.get(),
            "email": self.email.get(),
            "address": self.address.get(),
            "password": self.dob.get().replace("-", ""),
            "dob": self.dob.get(),
            "gender": self.gender.get(),
            "role": self.roles[self.role.current()],
            "department": self.departments[self.department.current()]
        })

        print(response)

        if response["success"]:
            self.initData()
            self.clearForm()
        else:
            messagebox.showerror("Lỗi", response["message"])

    def handleUpdateEmployee(self, id):
        response = employeeAPI.updateEmployee(id, {
            "code": self.code.get(),
            "name": self.name.get(),
            "phone": self.phone.get(),
            "email": self.email.get(),
            "address": self.address.get(),
            "dob": self.dob.get(),
            "gender": self.gender.get(),
            "role": self.roles[self.role.current()],
            "department": self.departments[self.department.current()]
        })

        print(response)

        if response["success"]:
            self.initData()
            self.clearForm()
            self.save_button.config(text="Tạo mới", command=self.handleSaveEmployee)
        else:
            messagebox.showerror("Lỗi", response["message"])

    def openCalendar(self, target):
        def selectDate():
            target.config(state="normal")
            target.delete(0, END)
            target.insert(0, cal.selection_get())
            target.config(state="readonly")
            top.destroy()

        top = Toplevel(self)
        cal = Calendar(top, selectmode="day", date_pattern="yyyy-mm-dd")
        cal.pack(pady=20)

        select_btn = Button(top, text="Chọn ngày", command=selectDate)
        select_btn.pack(pady=20)
