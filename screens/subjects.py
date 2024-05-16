from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

from API import subject

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

        # search bar
        self.searchBar = Entry(self)
        self.searchBar.pack(pady=10)

        # tree view
        self.columns = ("#1", "#2", "#3", "#4")
        self.tree = Treeview(self, columns=self.columns, show="headings")

        self.tree.column("#1", width=150)
        self.tree.heading("#1", text="Mã môn")
        self.tree.heading("#2", text="Tên môn")
        self.tree.heading("#3", text="Số tín chỉ")
        self.tree.heading("#4", text="Tỷ lệ điểm")

        self.initData()

        self.tree.bind("<Double-1>", self.editSubject)
        self.tree.bind("<Delete>", self.handleDeleteSubject)
        self.tree.pack(padx=10)

    def initData(self):
        response = subject.getAllSubjects()
        if "success" in response and response["success"]:
            for item in response["data"]:
                self.insertItemToTree(item)

    def insertItemToTree(self, subject):
        self.tree.insert("", "end", text=subject["id"], values=(subject["subjectCode"], subject["subjectName"], subject["credit"], subject["rate"]))

    def handleEditSubject(self, root, id, data):
        response = subject.updateSubject(id, data)
        if "success" in response and response["success"]:
            self.handleUpdateSubjectTree(id, data)
            messagebox.showinfo("Success", "Cập nhật môn học thành công")
            root.destroy()
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
        # create a top-level window
        top = Toplevel()
        top.title("Chỉnh sửa môn học")

        # get the selected item
        for selectedItem in self.tree.selection():
            item = self.tree.item(selectedItem)
            record = item['text']

        # get the selected item's data
        response = subject.getSubjectById(record)
        if "success" in response and response["success"]:
            data = response["data"][0]
        else:
            messagebox.showerror("Error", response["message"])
            return

        # Subject code
        subjectCodeLabel = Label(top, text="Mã môn:")
        subjectCodeLabel.grid(row=0, column=0, padx=10, pady=5)

        subjectCodeEntry = Entry(top)
        subjectCodeEntry.insert(0, data["subjectCode"])
        subjectCodeEntry.grid(row=0, column=1, padx=10, pady=5)

        # Subject name
        subjectNameLabel = Label(top, text="Tên môn:")
        subjectNameLabel.grid(row=1, column=0, padx=10, pady=5)

        subjectNameEntry = Entry(top)
        subjectNameEntry.insert(0, data["subjectName"])
        subjectNameEntry.grid(row=1, column=1, padx=10, pady=5)

        # Credit
        creditLabel = Label(top, text="Số tín chỉ:")
        creditLabel.grid(row=2, column=0, padx=10, pady=5)

        creditEntry = Entry(top)
        creditEntry.insert(0, data["credit"])
        creditEntry.grid(row=2, column=1, padx=10, pady=5)

        # Rate
        rateLabel = Label(top, text="Tỷ lệ điểm:")
        rateLabel.grid(row=3, column=0, padx=10, pady=5)

        rateEntry = Entry(top)
        rateEntry.insert(0, data["rate"])
        rateEntry.grid(row=3, column=1, padx=10, pady=5)

        # Update button
        updateButton = Button(top, text="Update", command=lambda: self.handleEditSubject(top, data["id"], {
            "subjectCode": subjectCodeEntry.get(),
            "subjectName": subjectNameEntry.get(),
            "credit": creditEntry.get(),
            "rate": rateEntry.get()
        }))
        updateButton.grid(row=4, column=0, columnspan=2, pady=10)


    def handleDeleteSubject(self, event):
        for selectedItem in self.tree.selection():
            item = self.tree.item(selectedItem)
            record = item['text']
            confirmation = messagebox.askquestion("Xác nhận xóa", "Bạn có chắc chắn muốn xóa không?")
            if confirmation == "yes":
                response = subject.deleteSubject(record)
                if "success" in response and response["success"]:
                    self.tree.delete(selectedItem)
                else:
                    messagebox.showerror("Error", response["message"])

class SubjectCreate(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.initUI()

    def initUI(self):
        # Subject label
        self.subjectLabel = Label(self, text="Tạo môn học", font=("Helvetica", 18))
        self.subjectLabel.pack(side="top", fill="x", pady=10, padx=10)

        self.formController = Frame(self)
        self.formController.pack(pady=10)

        # Subject code
        subjectCodeLabel = Label(self.formController, text="Mã môn:")
        subjectCodeLabel.grid(row=0, column=0, padx=10, pady=5)

        self.subjectCodeEntry = Entry(self.formController)
        self.subjectCodeEntry.grid(row=0, column=1, padx=10, pady=5)

        # Subject name
        subjectNameLabel = Label(self.formController, text="Tên môn:")
        subjectNameLabel.grid(row=1, column=0, padx=10, pady=5)

        self.subjectNameEntry = Entry(self.formController)
        self.subjectNameEntry.grid(row=1, column=1, padx=10, pady=5)

        # Credit
        creditLabel = Label(self.formController, text="Số tín chỉ:")
        creditLabel.grid(row=2, column=0, padx=10, pady=5)

        self.creditEntry = Entry(self.formController)
        self.creditEntry.grid(row=2, column=1, padx=10, pady=5)

        # Rate
        rateLabel = Label(self.formController, text="Tỷ lệ điểm:")
        rateLabel.grid(row=3, column=0, padx=10, pady=5)

        self.rateEntry = Entry(self.formController)
        self.rateEntry.grid(row=3, column=1, padx=10, pady=5)

        # Create button
        createButton = Button(self, text="Create", command=self.handleCreateSubject)
        createButton.pack(pady=10)

    def handleCreateSubject(self):
        subjectCode = self.subjectCodeEntry.get()
        subjectName = self.subjectNameEntry.get()
        credit = self.creditEntry.get()
        rate = self.rateEntry.get()

        if not subjectCode or not subjectName or not credit or not rate:
            messagebox.showerror("Error", "Vui lòng nhập đầy đủ thông tin")
            return

        response = subject.createSubject({
            "subjectCode": subjectCode,
            "subjectName": subjectName,
            "credit": credit,
            "rate": rate
        })

        if "success" in response and response["success"]:
            messagebox.showinfo("Success", "Tạo môn học thành công")
            self.controller.screens["Subjects"].insertItemToTree(response["data"][0])
            self.controller.showFrame("Subjects")
        else:
            messagebox.showerror("Error", response["message"])