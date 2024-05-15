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
        createYearButton = Button(self, text="Create Year", command=lambda: self.controller.showFrame("YearCreate"))
        createYearButton.pack(padx=10, pady=10)

        # List of years (replace with actual data retrieval)
        self.yearList = self.getYears()

        # tree view
        self.columns = ("#1", "#2")
        self.tree = Treeview(self, columns=self.columns, show="headings")


        self.tree.heading("#1", text="Năm học")
        self.tree.heading("#2", text="Học phí")

        for year in self.yearList:
            self.tree.insert("", "end", text=year["id"], values=(year["year"], year["tuition"]))

        self.tree.bind("<Double-1>", self.editYear)
        self.tree.bind("<Delete>", self.handleDeleteYear)
        self.tree.pack(padx=10)

    def getYears(self):
        return year.getAllYears()["data"] if year.getAllYears() else []

    def insertItemToTree(self, year):
        print(year)
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
                print("Delete ",record)
                year.deleteYear(record)
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

    def handleEditYear(self, root, selectedItem, id, name, tuition):
        response = year.updateYear(id, name, tuition)
        print(response)
        if response:
            root.destroy()
            self.tree.item(selectedItem, values=(name, tuition))
            self.controller.showFrame("Years")
        else:
            messagebox.showerror("Error", "Update failed")
