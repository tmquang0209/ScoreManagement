from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

from API import semester as semesterAPI, year as yearAPI

class Semester(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.initUI()

    def initUI(self):
        self.semesterLabel = Label(self, text="Quản lý học kỳ", font=("Helvetica", 18))
        self.semesterLabel.pack(side="top", fill="x", pady=10, padx=10)

        self.columns = ("#2", "#3")
        self.tree = Treeview(self, columns=self.columns, show="headings")

        self.tree.heading("#1", text="Tên học kỳ")
        self.tree.heading("#2", text="Năm học")

        self.tree.bind("<Double-1>", self.editSemester)
        self.tree.bind("<Delete>", self.deleteSemester)
        self.tree.pack(padx=10)

    def updateTree(self, semester):
        self.tree.selection()[0]
        self.tree.item(self.tree.selection()[0], values=(semester["semester"], semester["year"]["year"]))

    def insertItemToTree(self, semester):
        self.tree.insert("", "end", text=semester["id"], values=(semester["semester"], semester["year"]["year"]))

    def initData(self):
        # clear tree
        for i in self.tree.get_children():
            self.tree.delete(i)

        response = semesterAPI.getAllSemesters()

        if "success" in response and response["success"]:
            self.semesterList = response["data"]
            for semester in self.semesterList:
                self.insertItemToTree(semester)
        else:
            messagebox.showerror("Error", response["message"])

    def editSemester(self, event):
        def handleUpdateSemester(id, name, year):
            response = semesterAPI.updateSemester(id, {
                "semester": name,
                "year": year
            })

            if "success" in response and response["success"]:
                messagebox.showinfo("Success", response["message"])
                self.updateTree(response["data"][0])
                root.destroy()
            else:
                messagebox.showerror("Error", response["message"])

        yearsList = yearAPI.getAllYears()["data"] if yearAPI.getAllYears() else []
        id = event.widget.item(event.widget.selection()[0])["text"]
        semester = event.widget.item(event.widget.selection()[0])["values"]

        root = Toplevel(self)
        root.title("Edit Semester")

        semesterLabel = Label(root, text="Tên học kỳ")
        semesterLabel.grid(row=0, column=0, padx=10, pady=10)

        semesterEntry = Entry(root)
        semesterEntry.insert(0, semester[0])
        semesterEntry.grid(row=0, column=1, padx=10, pady=10)

        yearLabel = Label(root, text="Năm học")
        yearLabel.grid(row=1, column=0, padx=10, pady=10)

        yearCombobox = Combobox(root, values=[year["year"] for year in yearsList])
        yearCombobox.grid(row=1, column=1, padx=10, pady=10)
        yearCombobox.insert(0, semester[1])

        updateButton = Button(root, text="Update", command=lambda: handleUpdateSemester(id, semesterEntry.get(), yearsList[yearCombobox.current()]))
        updateButton.grid(row=2, column=0, columnspan=2, padx=10, pady=10)


    def deleteSemester(self, event):
        confirmation = messagebox.askyesno("Confirmation", "Bạn có muốn xóa học kỳ này không?")
        if confirmation:
            id = event.widget.item(event.widget.selection()[0])["text"]
            response = semesterAPI.deleteSemester(id)

            if "success" in response and response["success"]:
                messagebox.showinfo("Success", response["message"])
                self.tree.delete(event.widget.selection()[0])
            else:
                messagebox.showerror("Error", response["message"])

class SemesterCreate(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.initUI()

    def initUI(self):
        yearsList = yearAPI.getAllYears()["data"] if yearAPI.getAllYears() else []

        semesterLabel = Label(self, text="Thêm học kỳ", font=("Helvetica", 18))
        semesterLabel.pack(side="top", fill="x", pady=10, padx=10)

        fromController = Frame(self)
        fromController.pack(pady=10)

        semesterLabel = Label(fromController, text="Tên học kỳ")
        semesterLabel.grid(row=0, column=0, padx=10, pady=10)

        semesterEntry = Entry(fromController)
        semesterEntry.grid(row=0, column=1, padx=10, pady=10)

        yearLabel = Label(fromController, text="Năm học")
        yearLabel.grid(row=1, column=0, padx=10, pady=10)

        yearCombobox = Combobox(fromController, values=[year["year"] for year in yearsList])
        yearCombobox.grid(row=1, column=1, padx=10, pady=10)

        createButton = Button(self, text="Create", command=lambda: self.handleCreateSemester(semesterEntry.get(), yearsList[yearCombobox.current()]))
        createButton.pack(pady=10, padx=10)

    def handleCreateSemester(self, name, year):
        response = semesterAPI.createSemester({
            "semester": name,
            "year": year
        })
        
        if "success" in response and response["success"]:
            messagebox.showinfo("Success", response["message"])
            self.controller.screens["Semester"].initData()
            self.controller.showFrame("Semester")
        else:
            messagebox.showerror("Error", response["message"])
