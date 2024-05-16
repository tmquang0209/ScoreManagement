from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

from API import major

class Major(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.initUI()
        self.initData()

    def initUI(self):
        # Major label
        self.majorLabel = Label(self, text="Quản lý ngành học", font=("Helvetica", 18))
        self.majorLabel.pack(side="top", fill="x", pady=10, padx=10)

        # search bar
        self.searchBar = Entry(self)
        self.searchBar.pack(pady=10)

        # tree view
        self.columns = ("#1", "#2")
        self.tree = Treeview(self, columns=self.columns, show="headings")

        self.tree.column("#1", width=150)
        self.tree.heading("#1", text="Mã ngành")
        self.tree.heading("#2", text="Tên ngành")

        self.tree.bind("<Double-1>", self.editMajor)
        self.tree.bind("<Delete>", self.handleDeleteMajor)
        self.tree.pack(padx=10)

    def initData(self):
        # remove all items in tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        response = major.getAllMajors()
        if "success" in response and response["success"]:
            for item in response["data"]:
                self.insertItemToTree(item)

    def insertItemToTree(self, major):
        self.tree.insert("", "end", text=major["id"], values=(major["majorCode"], major["majorName"]))

    def handleEditMajor(self, root, id, data):
        response = major.updateMajor(id, data)
        if "success" in response and response["success"]:
            self.handleUpdateMajorTree(id, response["data"][0])
            messagebox.showinfo("Success", "Cập nhật ngành học thành công")
            root.destroy()
        else:
            messagebox.showerror("Error", response["message"])

    def handleUpdateMajorTree(self, id, data):
        for selectedItem in self.tree.selection():
            self.tree.item(selectedItem, text=data["id"], values=(data["majorCode"], data["majorName"]))

    def editMajor(self, event):
        item = event.widget.selection()[0]
        id = event.widget.item(item, "text")
        data = event.widget.item(item, "values")

        root = Toplevel(self)
        root.title("Cập nhật ngành học")

        form = Frame(root)
        form.pack(padx=10, pady=10)

        majorCodeLabel = Label(form, text="Mã ngành")
        majorCodeLabel.grid(row=0, column=0, padx=5, pady=10)

        majorCodeInput = Entry(form)
        majorCodeInput.insert(0, data[0])
        majorCodeInput.grid(row=0, column=1, padx=5, pady=10)

        majorNameLabel = Label(form, text="Tên ngành")
        majorNameLabel.grid(row=1, column=0, padx=5, pady=10)

        majorNameInput = Entry(form)
        majorNameInput.insert(0, data[1])
        majorNameInput.grid(row=1, column=1, padx=5, pady=10)

        submitButton = Button(form, text="Cập nhật", command=lambda: self.handleEditMajor(root, id, {
            "majorCode": majorCodeInput.get(),
            "majorName": majorNameInput.get()
        }))
        submitButton.grid(row=3, column=1, padx=5, pady=10)

    def handleDeleteMajor(self, event):
        item = self.tree.selection()[0]
        id = self.tree.item(item, "text")
        confirmation = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa ngành học này?")
        if not confirmation:
            return
        response = major.deleteMajor(id)
        if "success" in response and response["success"]:
            self.tree.delete(item)
            messagebox.showinfo("Success", "Xóa ngành học thành công")
        else:
            messagebox.showerror("Error", response["message"])

class MajorCreate(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.initUI()

    def initUI(self):
        # Major label
        self.majorLabel = Label(self, text="Thêm ngành học", font=("Helvetica", 18))
        self.majorLabel.pack(side="top", fill="x", pady=10, padx=10)

        # form
        form = Frame(self)
        form.pack(padx=10, pady=10)

        majorCodeLabel = Label(form, text="Mã ngành")
        majorCodeLabel.grid(row=0, column=0, padx=5, pady=10)

        self.majorCodeInput = Entry(form)
        self.majorCodeInput.grid(row=0, column=1, padx=5, pady=10)

        majorNameLabel = Label(form, text="Tên ngành")
        majorNameLabel.grid(row=1, column=0, padx=5, pady=10)

        self.majorNameInput = Entry(form)
        self.majorNameInput.grid(row=1, column=1, padx=5, pady=10)

        submitButton = Button(form, text="Thêm", command=self.handleCreateMajor)
        submitButton.grid(row=3, column=1, padx=5, pady=10)

    def handleCreateMajor(self):
        data = {
            "majorCode": self.majorCodeInput.get(),
            "majorName": self.majorNameInput.get(),
        }

        response = major.createMajor(data)
        if "success" in response and response["success"]:
            print(response)
            self.controller.screens["Major"].insertItemToTree(response["data"][0])
            messagebox.showinfo("Success", "Thêm ngành học thành công")
            self.controller.showFrame("Major")
        else:
            messagebox.showerror("Error", response["message"])
