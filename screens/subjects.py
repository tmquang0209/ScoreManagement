from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

from API import subject as subjectAPI

class Subjects(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.initUI()
        self.initData()

    def initUI(self):
        # Subject label
        self.subjectLabel = Label(self, text="Quản lý môn học", font=("Helvetica", 18))
        self.subjectLabel.pack(side="top", fill="x", pady=10, padx=10)

        # Form for creating or editing a subject
        self.formController = Frame(self)
        self.formController.pack(pady=10, fill=X)

        # Subject code
        self.subjectCodeLabel = Label(self.formController, text="Mã môn:")
        self.subjectCodeLabel.grid(row=0, column=0, padx=10, pady=5)

        self.subjectCodeEntry = Entry(self.formController)
        self.subjectCodeEntry.grid(row=0, column=1, padx=10, pady=5)

        # Subject name
        self.subjectNameLabel = Label(self.formController, text="Tên môn:")
        self.subjectNameLabel.grid(row=0, column=2, padx=10, pady=5)

        self.subjectNameEntry = Entry(self.formController)
        self.subjectNameEntry.grid(row=0, column=3, padx=10, pady=5)

        # Credit
        self.creditLabel = Label(self.formController, text="Số tín chỉ:")
        self.creditLabel.grid(row=0, column=4, padx=10, pady=5)

        self.creditEntry = Entry(self.formController)
        self.creditEntry.grid(row=0, column=5, padx=10, pady=5)

        # Rate
        self.rateLabel = Label(self.formController, text="Tỷ lệ điểm:")
        self.rateLabel.grid(row=0, column=6, padx=10, pady=5)

        self.rateEntry = Entry(self.formController)
        self.rateEntry.grid(row=0, column=7, padx=10, pady=5)

        # Create/Update button
        self.submitButton = Button(self.formController, text="Thêm", command=self.handleCreateOrUpdateSubject)
        self.submitButton.grid(row=4, column=0, pady=10)

        self.cancelButton = Button(self.formController, text="Hủy", command=self.clearForm)
        self.cancelButton.grid(row=4, column=1, pady=10)

        # Search bar
        self.searchBarFrame = Frame(self)
        self.searchBarFrame.pack(pady=10)

        Label(self.searchBarFrame, text="Tìm kiếm:").pack(side=LEFT)

        self.searchBar = Entry(self.searchBarFrame)
        self.searchBar.pack(side=LEFT, padx=10)

        searchButton = Button(self.searchBarFrame, text="Tìm kiếm", command=self.handleSearch)
        searchButton.pack(side=LEFT)

        # Tree view
        self.columns = ("#1", "#2", "#3", "#4")
        self.tree = Treeview(self, columns=self.columns, show="headings")

        self.tree.column("#1", width=150)
        self.tree.heading("#1", text="Mã môn")
        self.tree.heading("#2", text="Tên môn")
        self.tree.heading("#3", text="Số tín chỉ")
        self.tree.heading("#4", text="Tỷ lệ điểm")

        self.tree.bind("<Double-1>", self.editSubject)
        self.tree.bind("<Delete>", self.handleDeleteSubject)
        self.tree.pack(padx=10, pady=10, fill=BOTH, expand=True)

    def handleSearch(self):
        keyword = self.searchBar.get()
        response = subjectAPI.search(keyword)
        if "success" in response and response["success"]:
            for item in self.tree.get_children():
                self.tree.delete(item)

            for val in response["data"]:
                self.insertItemToTree(val)
        else:
            messagebox.showerror("Error", response["message"])

    def initData(self):
        # Remove all items in tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        response = subjectAPI.getAllSubjects()
        if "success" in response and response["success"]:
            for item in response["data"]:
                self.insertItemToTree(item)

    def insertItemToTree(self, subject):
        self.tree.insert("", "end", text=subject["id"], values=(subject["subjectCode"], subject["subjectName"], subject["credit"], subject["rate"]))

    def handleCreateOrUpdateSubject(self):
        subjectCode = self.subjectCodeEntry.get()
        subjectName = self.subjectNameEntry.get()
        credit = self.creditEntry.get()
        rate = self.rateEntry.get()

        if not subjectCode or not subjectName or not credit or not rate:
            messagebox.showerror("Error", "Vui lòng nhập đầy đủ thông tin")
            return

        if self.submitButton['text'] == "Thêm":
            response = subjectAPI.createSubject({
                "subjectCode": subjectCode,
                "subjectName": subjectName,
                "credit": credit,
                "rate": rate
            })

            if "success" in response and response["success"]:
                messagebox.showinfo("Success", "Tạo môn học thành công")
                self.insertItemToTree(response["data"][0])
                self.clearForm()
            else:
                messagebox.showerror("Error", response["message"])
        else:
            selectedItem = self.tree.selection()[0]
            subject_id = self.tree.item(selectedItem, "text")
            response = subjectAPI.updateSubject(subject_id, {
                "subjectCode": subjectCode,
                "subjectName": subjectName,
                "credit": credit,
                "rate": rate
            })
            if "success" in response and response["success"]:
                self.handleUpdateSubjectTree(subject_id, {
                    "subjectCode": subjectCode,
                    "subjectName": subjectName,
                    "credit": credit,
                    "rate": rate
                })
                messagebox.showinfo("Success", "Cập nhật môn học thành công")
                self.clearForm()
            else:
                messagebox.showerror("Error", response["message"])

    def handleUpdateSubjectTree(self, id, data):
        for selectedItem in self.tree.selection():
            item = self.tree.item(selectedItem)
            record = item['text']
            if record == id:
                self.tree.item(selectedItem, values=(data["subjectCode"], data["subjectName"], data["credit"], data["rate"]))
                break

    def editSubject(self, event):
        # Get the selected item
        selectedItem = self.tree.selection()[0]
        item = self.tree.item(selectedItem)
        record = item['text']

        # Get the selected item's data
        response = subjectAPI.getSubjectById(record)
        if "success" in response and response["success"]:
            data = response["data"][0]
        else:
            messagebox.showerror("Error", response["message"])
            return

        # Populate the form with the selected item's data
        self.subjectCodeEntry.delete(0, END)
        self.subjectCodeEntry.insert(0, data["subjectCode"])

        self.subjectNameEntry.delete(0, END)
        self.subjectNameEntry.insert(0, data["subjectName"])

        self.creditEntry.delete(0, END)
        self.creditEntry.insert(0, data["credit"])

        self.rateEntry.delete(0, END)
        self.rateEntry.insert(0, data["rate"])

        self.submitButton.config(text="Cập nhật")

    def handleDeleteSubject(self, event):
        selectedItem = self.tree.selection()[0]
        item = self.tree.item(selectedItem)
        record = item['text']
        confirmation = messagebox.askquestion("Xác nhận xóa", "Bạn có chắc chắn muốn xóa không?")
        if confirmation == "yes":
            response = subjectAPI.deleteSubject(record)
            if "success" in response and response["success"]:
                self.tree.delete(selectedItem)
                messagebox.showinfo("Success", "Xóa môn học thành công")
            else:
                messagebox.showerror("Error", response["message"])

    def clearForm(self):
        self.subjectCodeEntry.delete(0, END)
        self.subjectNameEntry.delete(0, END)
        self.creditEntry.delete(0, END)
        self.rateEntry.delete(0, END)
        self.submitButton.config(text="Thêm")