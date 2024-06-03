from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

from API import major

class Major(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.initUI()

    def initUI(self):
        # Major label
        self.majorLabel = Label(self, text="Quản lý ngành học", font=("Helvetica", 18))
        self.majorLabel.pack(side="top", fill="x", pady=10, padx=10)

        # Form for creating or editing a major
        self.formController = Frame(self)
        self.formController.pack(pady=10, fill=X)

        # Major code
        self.majorCodeLabel = Label(self.formController, text="Mã ngành:")
        self.majorCodeLabel.grid(row=0, column=0, padx=10, pady=5)

        self.majorCodeEntry = Entry(self.formController)
        self.majorCodeEntry.grid(row=0, column=1, padx=10, pady=5)

        # Major name
        self.majorNameLabel = Label(self.formController, text="Tên ngành:")
        self.majorNameLabel.grid(row=1, column=0, padx=10, pady=5)

        self.majorNameEntry = Entry(self.formController)
        self.majorNameEntry.grid(row=1, column=1, padx=10, pady=5)

        # Create/Update button
        self.submitButton = Button(self.formController, text="Thêm", command=self.handleCreateOrUpdateMajor)
        self.submitButton.grid(row=2, column=0, columnspan=2, pady=10)

        self.cancelButton = Button(self.formController, text="Hủy", command=self.clearForm)
        self.cancelButton.grid(row=2, column=2, pady=10)

        # Tree view
        self.columns = ("#1", "#2")
        self.tree = Treeview(self, columns=self.columns, show="headings")

        self.tree.column("#1", width=150)
        self.tree.heading("#1", text="Mã ngành")
        self.tree.heading("#2", text="Tên ngành")

        self.tree.bind("<Double-1>", self.editMajor)
        self.tree.bind("<Delete>", self.handleDeleteMajor)
        self.tree.pack(padx=10, pady=10, fill=BOTH, expand=True)

    def handleCreateOrUpdateMajor(self):
        majorCode = self.majorCodeEntry.get()
        majorName = self.majorNameEntry.get()

        if not majorCode or not majorName:
            messagebox.showerror("Error", "Vui lòng nhập đầy đủ thông tin")
            return

        if self.submitButton['text'] == "Thêm":
            response = major.createMajor({
                "majorCode": majorCode,
                "majorName": majorName
            })

            if "success" in response and response["success"]:
                messagebox.showinfo("Success", "Thêm ngành học thành công")
                self.insertItemToTree(response["data"][0])
                self.clearForm()
            else:
                messagebox.showerror("Error", response["message"])
        else:
            selectedItem = self.tree.selection()[0]
            major_id = self.tree.item(selectedItem, "text")
            response = major.updateMajor(major_id, {
                "majorCode": majorCode,
                "majorName": majorName
            })
            if "success" in response and response["success"]:
                self.handleUpdateMajorTree(major_id, {
                    "majorCode": majorCode,
                    "majorName": majorName
                })
                messagebox.showinfo("Success", "Cập nhật ngành học thành công")
                self.clearForm()
            else:
                messagebox.showerror("Error", response["message"])

    def handleUpdateMajorTree(self, id, data):
        for selectedItem in self.tree.selection():
            item = self.tree.item(selectedItem)
            record = item['text']
            if record == id:
                self.tree.item(selectedItem, values=(data["majorCode"], data["majorName"]))
                break

    def editMajor(self, event):
        # Get the selected item
        selectedItem = self.tree.selection()[0]
        item = self.tree.item(selectedItem)
        record = item['text']

        # Get the selected item's data
        response = major.getMajorById(record)
        if "success" in response and response["success"]:
            data = response["data"][0]
        else:
            messagebox.showerror("Error", response["message"])
            return

        # Populate the form with the selected item's data
        self.majorCodeEntry.delete(0, END)
        self.majorCodeEntry.insert(0, data["majorCode"])

        self.majorNameEntry.delete(0, END)
        self.majorNameEntry.insert(0, data["majorName"])

        self.submitButton.config(text="Cập nhật")

    def handleDeleteMajor(self, event):
        selectedItem = self.tree.selection()[0]
        item = self.tree.item(selectedItem)
        record = item['text']
        confirmation = messagebox.askquestion("Xác nhận xóa", "Bạn có chắc chắn muốn xóa ngành học này?")
        if confirmation == "yes":
            response = major.deleteMajor(record)
            if "success" in response and response["success"]:
                self.tree.delete(selectedItem)
                messagebox.showinfo("Success", "Xóa ngành học thành công")
            else:
                messagebox.showerror("Error", response["message"])

    def clearForm(self):
        self.majorCodeEntry.delete(0, END)
        self.majorNameEntry.delete(0, END)
        self.submitButton.config(text="Thêm")

    def initData(self):
        # Remove all items in tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        response = major.getAllMajors()
        if "success" in response and response["success"]:
            for item in response["data"]:
                self.insertItemToTree(item)

    def insertItemToTree(self, major):
        self.tree.insert("", "end", text=major["id"], values=(major["majorCode"], major["majorName"]))