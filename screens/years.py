from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from API import year as yearAPI, semester as semesterAPI

class Years(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Year label
        self.yearLabel = Label(self, text="Quản lý năm học", font=("Helvetica", 18))
        self.yearLabel.pack(side="top", fill="x", pady=10, padx=10)

        # Create year button
        # createYearButton = Button(self, text="Create Year", command=lambda: self.controller.showFrame("YearCreate"))
        # createYearButton.pack(padx=10, pady=10)

        self.yearFrame = Frame(self)
        self.yearFrame.pack(padx=10, pady=10, side="left")

        # Create form
        self.initCreateForm()

        # List of years (replace with actual data retrieval)
        self.yearList = self.getYears()

        # Initialize tree view
        self.initTreeUI()

        # Semester frame
        self.semesterFrame = Frame(self)
        self.semesterFrame.pack(padx=10, pady=10, side="right")

        self.semesterForm = Frame(self.semesterFrame)
        self.semesterForm.pack(padx=10, pady=10)

        Label(self.semesterForm, text="Học kỳ").grid(row=0, column=0, padx=10, pady=10)
        semesterNameInput = Entry(self.semesterForm)
        semesterNameInput.grid(row=0, column=1, padx=10, pady=10)

        createSemesterButton = Button(self.semesterForm, text="Create Semester", command=lambda: self.handleCreateSemester(semesterNameInput.get()))
        createSemesterButton.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        # init semester treeview
        self.initSemesterTreeUI()

    def handleCreateSemester(self, name):
        # get year selected
        yearSelected = self.tree.selection()[0] if self.tree.selection() else None
        yearId = self.tree.item(yearSelected)["text"] if yearSelected else None

        if yearId:
            # find year by id in yearList
            year = None
            for item in self.yearList:
                if item["id"] == yearId:
                    year = item
                    break

            if name == "":
                messagebox.showerror("Error", "Vui lòng nhập tên học kỳ")
                return

            response = semesterAPI.createSemester({
                "semester": name,
                "year": year
            })


            if response["success"]:
                self.initSemesterTree(yearId)
            else:
                messagebox.showerror("Error", response["message"])
        else:
            messagebox.showerror("Error", "Vui lòng chọn năm học")

    def initCreateForm(self):
        # Create year form
        createYearForm = Frame(self.yearFrame)
        createYearForm.pack(padx=10, pady=10)

        yearLabel = Label(createYearForm, text="Năm học")
        yearLabel.grid(row=0, column=0, padx=10, pady=10)

        yearInput = Entry(createYearForm)
        yearInput.grid(row=0, column=1, padx=10, pady=10)

        tuitionLabel = Label(createYearForm, text="Học phí")
        tuitionLabel.grid(row=1, column=0, padx=10, pady=10)

        tuitionInput = Spinbox(createYearForm, from_=0, to=1000000000, increment=1000000)
        tuitionInput.grid(row=1, column=1, padx=10, pady=10)

        submitButton = Button(createYearForm, text="Create", command=lambda: self.handleCreateYear(yearInput.get(), tuitionInput.get()))
        submitButton.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def handleCreateYear(self, year, tuition):
        response = yearAPI.createYear(year, tuition)

        if response["success"]:
            self.initData()
        else:
            messagebox.showerror("Error", response["message"])

    def initTreeUI(self):
        # tree view
        self.columns = ("#1", "#2")
        self.tree = Treeview(self.yearFrame, columns=self.columns, show="headings")

        self.tree.heading("#1", text="Năm học")
        self.tree.heading("#2", text="Học phí")

        self.tree.bind("<Double-1>", self.editYear)
        self.tree.bind("<Delete>", self.handleDeleteYear)
        self.tree.bind("<<TreeviewSelect>>", self.updateSemesterTree)
        self.tree.pack(padx=10)

    def updateSemesterTree(self, event):
        for selectedItem in self.tree.selection():
            item = self.tree.item(selectedItem)
            record = item['text']
            self.initSemesterTree(record)

    def initSemesterTree(self, yearId):

        response = semesterAPI.getSemesterByYear(yearId)

        if response["success"]:
            # remove all items in tree
            for item in self.semesterTree.get_children():
                self.semesterTree.delete(item)
            for item in response["data"]:
                self.insertSemesterToTree(item)

    def insertSemesterToTree(self, semester):
        self.semesterTree.insert("", "end", text=semester["id"], values=(semester["semester"],))

    def initSemesterTreeUI(self):
        # tree view
        self.semesterColumns = ("#1")
        self.semesterTree = Treeview(self.semesterFrame, columns=self.semesterColumns, show="headings")

        self.semesterTree.heading("#1", text="Tên học kỳ")

        self.semesterTree.bind("<Double-1>", self.editSemester)
        self.semesterTree.bind("<Delete>", self.handleDeleteSemester)
        # self.tree.bind("<<TreeviewSelect>>", self.updateEditForm)
        self.semesterTree.pack(padx=10)

    def handleDeleteSemester(self, event):
        for selectedItem in self.semesterTree.selection():
            item = self.semesterTree.item(selectedItem)
            record = item['text']
            confirmation = messagebox.askquestion("Xác nhận xóa", "Bạn có chắc chắn muốn xóa không?")
            if confirmation == "yes":
                semesterAPI.deleteSemester(record)
                self.semesterTree.delete(selectedItem)

    def getYears(self):
        return yearAPI.getAllYears()["data"] if yearAPI.getAllYears() else []

    def initData(self):
        # remove all items in tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        response = yearAPI.getAllYears()
        if "success" in response and response["success"]:
            for item in response["data"]:
                self.insertItemToTree(item)

    def insertItemToTree(self, year):
        self.tree.insert("", "end", text=year["id"], values=(year["year"], year["tuition"]))

    def handleViewYear(self, event):
        for selectedItem in self.tree.selection():
            item = self.tree.item(selectedItem)
            record = item['text']
            self.controller.showFrame("YearUpdate", record)

    def handleDeleteYear(self, event):
        for selectedItem in self.tree.selection():
            item = self.tree.item(selectedItem)
            record = item['text']
            confirmation = messagebox.askquestion("Xác nhận xóa", "Bạn có chắc chắn muốn xóa không?")
            if confirmation == "yes":
                yearAPI.deleteYear(record)
                self.tree.delete(selectedItem)

    def editYear(self, event):
        editRoot = Tk()
        editRoot.title("Edit Year")
        editRoot.geometry("400x200")

        yearLabel = Label(editRoot, text="Năm học")
        yearLabel.grid(row=0, column=0, padx=10, pady=10)

        yearInput = Entry(editRoot)
        yearInput.grid(row=0, column=1, padx=10, pady=10)

        tuitionLabel = Label(editRoot, text="Học phí")
        tuitionLabel.grid(row=1, column=0, padx=10, pady=10)

        tuitionInput = Spinbox(editRoot, from_=0, to=1000000000, increment=1000000)
        tuitionInput.grid(row=1, column=1, padx=10, pady=10)

        for selectedItem in self.tree.selection():
            item = self.tree.item(selectedItem)
            record = item['values']
            yearInput.insert(0, record[0])
            tuitionInput.insert(0, record[1])

            submitButton = Button(editRoot, text="Update", command=lambda: self.handleEditYear(editRoot, selectedItem, item["text"], yearInput.get(), tuitionInput.get()))
            submitButton.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        editRoot.mainloop()

    def editSemester(self, event):
        def handleUpdateSemester(id, name):
            year = None
            for selectedItem in self.tree.selection():
                item = self.tree.item(selectedItem)
                year = item['text']
                break

            yearData = None
            for item in self.yearList:
                if item["id"] == year:
                    yearData = item
                    break

            response = semesterAPI.updateSemester(id, {
                "semester": name,
                "year": yearData
            })


            if "success" in response and response["success"]:
                messagebox.showinfo("Success", response["message"])
                self.initSemesterTree(year)
                root.destroy()
            else:
                messagebox.showerror("Error", response["message"])

        id = event.widget.item(event.widget.selection()[0])["text"]
        semester = event.widget.item(event.widget.selection()[0])["values"]

        root = Toplevel(self)
        root.title("Edit Semester")
        root.geometry("400x200")

        semesterLabel = Label(root, text="Tên học kỳ")
        semesterLabel.grid(row=0, column=0, padx=10, pady=10)

        semesterEntry = Entry(root)
        semesterEntry.insert(0, semester[0])
        semesterEntry.grid(row=0, column=1, padx=10, pady=10)

        updateButton = Button(root, text="Update", command=lambda: handleUpdateSemester(id, semesterEntry.get()))
        updateButton.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def handleEditYear(self, root, selectedItem, id, name, tuition):
        response = yearAPI.updateYear(id, name, tuition)

        if response:
            root.destroy()
            self.tree.item(selectedItem, values=(name, tuition))
            self.controller.showFrame("Years")
        else:
            messagebox.showerror("Error", "Update failed")
