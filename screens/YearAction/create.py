from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

from API.year import createYear as createYearAPI

class YearCreate(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Year label
        self.yearLabel = Label(self, text="Tạo năm học", font=("Helvetica", 18))
        self.yearLabel.pack(side="top", fill="x", pady=10, padx=10)

        # Year entry
        self.yearVar = StringVar()
        yearLabel = Label(self, text="Năm học:")
        yearLabel.pack()
        yearEntry = Entry(self, textvariable=self.yearVar)
        yearEntry.pack()

        # Tuition entry
        self.tuitionVar = StringVar()
        tuitionLabel = Label(self, text="Học phí:")
        tuitionLabel.pack()
        tuitionEntry = Spinbox(self, from_=0, to=1000000000, increment=1000000, textvariable=self.tuitionVar)
        tuitionEntry.pack()

        # Create year button
        createYearButton = Button(self, text="Tạo", command=self.createYear)
        createYearButton.pack(pady=10)

        # Back button
        backButton = Button(self, text="Back", command=lambda: self.controller.showFrame("Years"))
        backButton.pack(pady=10)

    def createYear(self):
        year = self.yearVar.get()
        tuition = self.tuitionVar.get()

        # Input validation (add checks for empty fields or invalid formats)
        if not year or not tuition:
            messagebox.showerror("Lỗi", "Vui lòng nhập đủ thông tin.")
            return

        # API call to create year (replace with your actual API interaction)
        response = createYearAPI(year, tuition)
        print(response)

        if response['success'] == True:
            messagebox.showinfo("Success", response['message'])
            self.controller.screens["Years"].insertItemToTree(response["data"][0])
            self.controller.showFrame("Years")
        else:
            messagebox.showerror("Error", response['message'])