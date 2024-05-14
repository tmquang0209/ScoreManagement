from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from API import year

class Years(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Year label
        self.yearLabel = Label(self, text="Quản lý năm học", font=("Helvetica", 18))
        self.yearLabel.pack(side="top", fill="x", pady=10, padx=10)

        # Create year button
        createYearButton = Button(self, text="Create Year", command=lambda: self.controller.show_frame("years.Create"))
        createYearButton.pack(padx=10, pady=10)

        # List of years (replace with actual data retrieval)
        self.yearList = self.getYears()
        print(self.yearList)

        # tree view
        self.columns = ("#1", "#2", "#3")
        self.tree = Treeview(self, columns=self.columns, show="headings")

        self.tree.heading("#1", text="STT")
        self.tree.heading("#2", text="Năm học")
        self.tree.heading("#3", text="Học phí")

        for year in self.yearList:
            self.tree.insert("", "end", values=(year["id"], year["year"], year["tuition"]))

        self.tree.bind("<<TreeviewSelect>>", self.viewYear)
        self.tree.pack(padx=10)

    def getYears(self):
        return year.getAllYears()["data"] if year.getAllYears() else []


    def viewYear(self, event):
        for selectedItem in self.tree.selection():
            item = self.tree.item(selectedItem)
            record = item['values']
            print(record)

    def createYear(self):
        yearFrame = Frame(yearRoot)
        yearFrame.pack()

        yearLabel = Label(yearFrame, text="Năm học", padding=5)
        yearLabel.grid(row=0, column=0)

        yearEntry = Entry(yearFrame)
        yearEntry.grid(row=0, column=1)

    def editYear(self):
        yearLabel = Label(yearRoot, text="Chỉnh sửa năm học", font=15, padding=10)
        yearLabel.pack()