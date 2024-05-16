from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry

import json

from API import user
from modules import localStorage

class PersonalInfo(Frame):
    def __init__ (self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.localStorage = localStorage

        self.controller.config(menu=None)

    def clearPersonalInfo(self):
            for widget in self.winfo_children():
                widget.destroy()

    def preparePersonalInfo(self):
        personalInfo = self.localStorage.getItem("user")
        personalInfo = json.loads(personalInfo) if personalInfo else {}

        self.userName = personalInfo["name"] if "name" in personalInfo else ""

        # Welcome label
        self.welcomeLabel = Label(self, text="Thông tin cá nhân", font=("Helvetica", 18))
        self.welcomeLabel.pack(side="top", fill="x", pady=10, padx=10)

        formContainer = Frame(self, padding=10)
        formContainer.pack()

        # Code
        codeLabel = Label(formContainer, text="Mã: ")
        codeLabel.grid(row=0, column=0, padx=10, pady=5)

        codeEntry = Entry(formContainer)
        codeEntry.grid(row=0, column=1, padx=10, pady=5)
        codeEntry.insert(0, personalInfo["code"] if "code" in personalInfo else personalInfo["teacherCode"] if "teacherCode" in personalInfo else "")
        codeEntry.config(state="disabled")

        # Name
        nameLabel = Label(formContainer, text="Họ và tên: ")
        nameLabel.grid(row=1, column=0, padx=10, pady=5)

        nameEntry = Entry(formContainer)
        nameEntry.grid(row=1, column=1, padx=10, pady=5)
        nameEntry.insert(0, personalInfo["name"] if "name" in personalInfo else "")
        nameEntry.config(state="disabled")

        # Role
        roleLabel = Label(formContainer, text="Chức vụ: ")
        roleLabel.grid(row=3, column=0, padx=10, pady=5)

        roleEntry = Entry(formContainer)
        roleEntry.grid(row=3, column=1, padx=10, pady=5)
        roleEntry.insert(0, personalInfo["role"]["name"] if "role" in personalInfo else "")
        roleEntry.config(state="disabled")

        # Email
        emailLabel = Label(formContainer, text="Email: ")
        emailLabel.grid(row=2, column=0, padx=10, pady=5)

        emailEntry = Entry(formContainer)
        emailEntry.grid(row=2, column=1, padx=10, pady=5)
        emailEntry.insert(0, personalInfo["email"] if "email" in personalInfo else "")

        # Phone
        phoneLabel = Label(formContainer, text="Số điện thoại: ")
        phoneLabel.grid(row=4, column=0, padx=10, pady=5)

        phoneEntry = Entry(formContainer)
        phoneEntry.grid(row=4, column=1, padx=10, pady=5)
        phoneEntry.insert(0, personalInfo["phone"] if "phone" in personalInfo else "")

        # Address
        addressLabel = Label(formContainer, text="Địa chỉ: ")
        addressLabel.grid(row=5, column=0, padx=10, pady=5)

        addressEntry = Entry(formContainer)
        addressEntry.grid(row=5, column=1, padx=10, pady=5)
        addressEntry.insert(0, personalInfo["address"] if "address" in personalInfo and personalInfo["address"] != None else "")

        # dob
        dobLabel = Label(formContainer, text="Ngày sinh: ")
        dobLabel.grid(row=6, column=0, padx=10, pady=5)

        dobEntry = Entry(formContainer)
        dobEntry.grid(row=6, column=1, padx=10, pady=5)
        dobEntry.insert(0, personalInfo["dob"] if "dob" in personalInfo and personalInfo["dob"] != None else "")
        dobEntry.config(state="readonly")

        # Button to open calendar
        dobButton = Button(formContainer, text="Chọn ngày", command=lambda: self.openCalendar(dobEntry))
        dobButton.grid(row=6, column=2, padx=10, pady=5)

        # submit button
        submitButton = Button(formContainer, text="Cập nhật", command=lambda: self.updatePersonalInfo(personalInfo["id"], emailEntry.get(), phoneEntry.get(), addressEntry.get(), dobEntry.get()))
        submitButton.grid(row=7, column=0, columnspan=2, pady=10)

    def openCalendar(self, dobEntry):
        personalInfo = self.localStorage.getItem("user")
        personalInfo = json.loads(personalInfo) if personalInfo else {}
        birthYear = personalInfo["dob"].split("-")[0] if "dob" in personalInfo and personalInfo["dob"] != None else 2000
        birthMonth = personalInfo["dob"].split("-")[1] if "dob" in personalInfo and personalInfo["dob"] != None else 1
        birthDay = personalInfo["dob"].split("-")[2] if "dob" in personalInfo and personalInfo["dob"] != None else 1

        top = Toplevel(self)
        cal = Calendar(top, selectmode="day", year=int(birthYear), month=int(birthMonth), day=int(birthDay))
        cal.pack(padx=10, pady=10)

        def grab_date():
            date = cal.selection_get()
            formatted_date = date.strftime('%Y-%m-%d')
            dobEntry.config(state="normal")
            dobEntry.delete(0, END)
            dobEntry.insert(0, formatted_date)
            dobEntry.config(state="readonly")
            top.destroy()

        Button(top, text="Chọn", command=grab_date).pack(pady=10)

    def updatePersonalInfo(self, id, email, phone, address, dob):
        # Here you would include the logic to update the personal information
        print(f"Updating info: Email: {email}, Phone: {phone}, Address: {address}, DOB: {dob}")
        response = user.updateInfo(id, {
            "email": email,
            "phone": phone,
            "address": address,
            "dob": dob
        })
        if response["success"]:
            messagebox.showinfo("Thành công", "Cập nhật thông tin thành công")
            localStorage.setItem("user", json.dumps(response["data"][0]))
        else:
            messagebox.showerror("Lỗi", "Cập nhật thông tin thất bại")