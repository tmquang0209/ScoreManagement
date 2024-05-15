from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

import json

from modules import localStorage

from API import user

class ChangePassword(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.controller.config(menu=None)

        self.oldPasswordVar = StringVar()
        self.newPasswordVar = StringVar()
        self.confirmPasswordVar = StringVar()

        self.prepareChangePassword()

    def prepareChangePassword(self):
        self.changePasswordLabel = Label(self, text="Đổi mật khẩu", font=("Helvetica", 18))
        self.changePasswordLabel.grid(row=0, column=0, columnspan=3, pady=10, padx=10)

        formContainer = Frame(self, padding=10)
        formContainer.grid(row=1, column=3, columnspan=1, pady=10)

        # Old password
        oldPasswordLabel = Label(formContainer, text="Mật khẩu cũ: ")
        oldPasswordLabel.grid(row=0, column=0, padx=10, pady=5)

        oldPasswordEntry = Entry(formContainer, textvariable=self.oldPasswordVar, show="*")
        oldPasswordEntry.grid(row=0, column=1, padx=10, pady=5)

        # New password
        newPasswordLabel = Label(formContainer, text="Mật khẩu mới: ")
        newPasswordLabel.grid(row=1, column=0, padx=10, pady=5)

        newPasswordEntry = Entry(formContainer, textvariable=self.newPasswordVar, show="*")
        newPasswordEntry.grid(row=1, column=1, padx=10, pady=5)

        # Confirm password
        confirmPasswordLabel = Label(formContainer, text="Xác nhận mật khẩu: ")
        confirmPasswordLabel.grid(row=2, column=0, padx=10, pady=5)

        confirmPasswordEntry = Entry(formContainer, textvariable=self.confirmPasswordVar, show="*")
        confirmPasswordEntry.grid(row=2, column=1, padx=10, pady=5)

        # Change password button
        changePasswordButton = Button(formContainer, text="Đổi mật khẩu", command=self.handleChangePassword)
        changePasswordButton.grid(row=3, column=1, pady=10)

    def handleChangePassword(self):
        oldPassword = self.oldPasswordVar.get()
        newPassword = self.newPasswordVar.get()
        confirmPassword = self.confirmPasswordVar.get()

        if not oldPassword or not newPassword or not confirmPassword:
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin.")
            return

        if newPassword != confirmPassword:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp.")
            return

        userId = json.loads(localStorage.getItem("user"))["id"]

        response = user.changePassword(userId, {
            "oldPassword": oldPassword,
            "newPassword": newPassword,
            "confirmPassword": confirmPassword
        })

        print(response)

        if response['success'] == True:
            messagebox.showinfo("Thành công", "Thay đổi mật khẩu thành công.")
            self.controller.showFrame("Home")
        else:
            messagebox.showerror("Lỗi", response['message'])
            return
