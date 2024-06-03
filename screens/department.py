from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from API import department

class Department(Frame):
    def __init__ (self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.initUI()

    def initUI(self):
        # Title
        title = Label(self, text="Danh sách phòng ban", font=("Helvetica", 18))
        title.pack(side="top", fill="x", pady=10, padx=10)

        # Form for creating or editing a department
        self.form = Frame(self)
        self.form.pack(padx=10, pady=10, fill=X)

        self.codeLabel = Label(self.form, text="Mã phòng ban")
        self.codeLabel.grid(row=0, column=0, padx=5, pady=10)

        self.codeInput = Entry(self.form, width=50)
        self.codeInput.grid(row=0, column=1, padx=5, pady=10)

        self.nameLabel = Label(self.form, text="Tên phòng ban")
        self.nameLabel.grid(row=1, column=0, padx=5, pady=10)

        self.nameInput = Entry(self.form, width=50)
        self.nameInput.grid(row=1, column=1, padx=5, pady=10)

        self.submitButton = Button(self.form, text="Thêm", command=self.handleCreateOrUpdateDepartment)
        self.submitButton.grid(row=2, column=1, padx=5, pady=10)

        self.cancelButton = Button(self.form, text="Hủy", command=self.clearForm)
        self.cancelButton.grid(row=2, column=0, padx=5, pady=10)

        # Treeview
        self.tree = Treeview(self, columns=("ID", "Code", "Name"), show="headings")
        self.tree.column("ID", width=100)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Code", text="Mã phòng ban")
        self.tree.heading("Name", text="Tên phòng ban")
        self.tree.pack(pady=10, fill=BOTH, expand=True)

        self.tree.bind("<Double-1>", self.editDepartment)
        self.tree.bind("<Delete>", self.handleDelete)

    def initData(self):
        # remove all items in tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        response = department.getDepartments()

        if "success" in response and response["success"]:
            for item in response["data"]:
                self.insertItemToTree(item)

    def handleUpdateDepartmentTree(self, id, data):
        for selectedItem in self.tree.selection():
            self.tree.item(selectedItem, values=(id, data["code"], data["name"]))

    def insertItemToTree(self, department):
        self.tree.insert("", "end", text=department["id"], values=(department["id"], department["code"], department["name"]))

    def handleCreateOrUpdateDepartment(self):
        code = self.codeInput.get()
        name = self.nameInput.get()

        if self.submitButton['text'] == "Thêm":
            response = department.createDepartment({"code": code, "name": name})
            if response["success"]:
                self.codeInput.delete(0, END)
                self.nameInput.delete(0, END)
                self.insertItemToTree(response["data"][0])
                messagebox.showinfo("Success", "Thêm phòng ban thành công")
            else:
                messagebox.showerror("Error", response["message"])
        else:
            selectedItem = self.tree.selection()[0]
            department_id = self.tree.item(selectedItem, "text")
            response = department.updateDepartment(department_id, {"code": code, "name": name})
            if response["success"]:
                self.handleUpdateDepartmentTree(department_id, {"code": code, "name": name})
                messagebox.showinfo("Success", "Cập nhật phòng ban thành công")
                self.clearForm()
            else:
                messagebox.showerror("Error", response["message"])

    def editDepartment(self, event):
        item = event.widget.selection()[0]
        data = event.widget.item(item, "values")

        self.codeInput.delete(0, END)
        self.codeInput.insert(0, data[1])
        self.nameInput.delete(0, END)
        self.nameInput.insert(0, data[2])

        self.submitButton.config(text="Cập nhật")

    def handleDelete(self, event):
        item = event.widget.selection()[0]
        data = event.widget.item(item, "values")

        confirmation = messagebox.askyesnocancel("Xác nhận", "Bạn có chắc chắn muốn xóa phòng ban này không?")
        if confirmation:
            response = department.deleteDepartment(data[0])
            if response["success"]:
                self.tree.delete(item)
                messagebox.showinfo("Success", "Xóa phòng ban thành công")
            else:
                messagebox.showerror("Error", response["message"])

    def clearForm(self):
        self.codeInput.delete(0, END)
        self.nameInput.delete(0, END)
        self.submitButton.config(text="Thêm")