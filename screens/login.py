from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

from API import user
class Login(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.controller.config(menu=None)

        self.usernameVar = StringVar()
        self.passwordVar = StringVar()

        self.loginLabel = Label(self, text="Login", font=("Helvetica", 18))
        self.loginLabel.pack(side="top", fill="x", pady=10)

        usernameLabel = Label(self, text="Username:")
        usernameLabel.pack()
        usernameEntry = Entry(self, textvariable=self.usernameVar)
        usernameEntry.pack()

        passwordLabel = Label(self, text="Password:")
        passwordLabel.pack()
        passwordEntry = Entry(self, textvariable=self.passwordVar, show="*")
        passwordEntry.pack()

        loginButton = Button(self, text="Login", command=self.handleLogin)
        loginButton.pack()

    def handleLogin(self):
        username = self.usernameVar.get()
        password = self.passwordVar.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password.")
            return

        response = user.userLogin(username, password)

        if response.get("success"):
            self.controller.token = self.controller.checkToken()
            self.controller.screens["Home"].prepareHome()
            self.controller.screens["PersonalInfo"].preparePersonalInfo()
            self.controller.showFrame("Home")
        else:
            messagebox.showerror("Error", "Invalid login credentials. Please try again.")
