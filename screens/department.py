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
        title = Label(self, text="Danh sách phòng ban", font=("Helvetica", 18))
        title.pack(side="top", fill="x", pady=10, padx=10)

        # Tree
        self.tree = Treeview(self, columns=("ID", "Code", "Name"), show="headings")
        self.tree.column("ID", width=100)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Code", text="Mã phòng ban")
        self.tree.heading("Name", text="Tên phòng ban")
        self.tree.pack()

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

    def handleEditDepartment(self, root, id, data):
        response = department.updateDepartment(id, data)
        if response["success"]:
            self.handleUpdateDepartmentTree(id, data)
            messagebox.showinfo("Success", "Cập nhật phòng ban thành công")
            root.destroy()
        else:
            messagebox.showerror("Error", response["message"])

    def editDepartment(self, event):
        item = event.widget.selection()[0]
        data = event.widget.item(item, "values")

        root = Toplevel(self)
        root.title("Chỉnh sửa phòng ban")

        form = Frame(root)
        form.pack(padx=10, pady=10)

        codeLabel = Label(form, text="Mã phòng ban")
        codeLabel.grid(row=0, column=0, padx=5, pady=10)

        codeInput = Entry(form)
        codeInput.grid(row=0, column=1, padx=5, pady=10)

        nameLabel = Label(form, text="Tên phòng ban")
        nameLabel.grid(row=1, column=0, padx=5, pady=10)

        nameInput = Entry(form)
        nameInput.grid(row=1, column=1, padx=5, pady=10)

        codeInput.insert(0, data[1])
        nameInput.insert(0, data[2])

        submitButton = Button(form, text="Cập nhật", command=lambda: self.handleEditDepartment(root, data[0], {
            "code": codeInput.get(),
            "name": nameInput.get()
        }))
        submitButton.grid(row=2, column=1, padx=5, pady=10)

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

class DepartmentCreate(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.initUI()

    def initUI(self):
        self.title = Label(self, text="Thêm phòng ban", font=("Helvetica", 18))
        self.title.pack(side="top", fill="x", pady=10, padx=10)

        self.form = Frame(self)
        self.form.pack(padx=10, pady=10)

        self.codeLabel = Label(self.form, text="Mã phòng ban")
        self.codeLabel.grid(row=0, column=0, padx=5, pady=10)

        self.codeInput = Entry(self.form)
        self.codeInput.grid(row=0, column=1, padx=5, pady=10)

        self.nameLabel = Label(self.form, text="Tên phòng ban")
        self.nameLabel.grid(row=1, column=0, padx=5, pady=10)

        self.nameInput = Entry(self.form)
        self.nameInput.grid(row=1, column=1, padx=5, pady=10)

        submitButton = Button(self.form, text="Thêm", command=lambda: self.handleCreateDepartment({
            "code": self.codeInput.get(),
            "name": self.nameInput.get()
        }))
        submitButton.grid(row=2, column=1, padx=5, pady=10)

    def handleCreateDepartment(self, data):
        response = department.createDepartment(data)
        print(response)
        if response["success"]:
            self.codeInput.delete(0, END)
            self.nameInput.delete(0, END)

            self.controller.screens["Department"].insertItemToTree(response["data"][0])
            messagebox.showinfo("Success", "Thêm phòng ban thành công")
            self.controller.showFrame("Department")
        else:
            messagebox.showerror("Error", response["message"])