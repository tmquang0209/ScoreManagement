from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from API import user

class Login(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.controller.config(menu=None)

        self.usernameVar = StringVar()  # Variable for username entry
        self.passwordVar = StringVar()  # Variable for password entry

        # Login label
        self.loginLabel = Label(self, text="Login", font=("Helvetica", 18))
        self.loginLabel.pack(side="top", fill="x", pady=10)

        # Username label and entry
        usernameLabel = Label(self, text="Username:")
        usernameLabel.pack()
        usernameEntry = Entry(self, textvariable=self.usernameVar)
        usernameEntry.pack()

        # Password label and entry (consider using a password-masking widget)
        passwordLabel = Label(self, text="Password:")
        passwordLabel.pack()
        passwordEntry = Entry(self, textvariable=self.passwordVar, show="*")  # Use asterisk for password masking
        passwordEntry.pack()

        # Login button
        loginButton = Button(self, text="Login", command=self.handleLogin)
        loginButton.pack()

    def handleLogin(self):
        username = self.usernameVar.get()
        password = self.passwordVar.get()

        # Input validation (add checks for empty fields or invalid formats)
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password.")
            return

        # API call to verify login credentials (replace with your actual API interaction)
        response = user.userLogin(username, password)

        if "success" in response and response['success'] == True:
            # Call fetchUserInfo to update user information
            self.controller.screens["Home"].prepareHome()
            self.controller.screens["PersonalInfo"].preparePersonalInfo()
            self.controller.showFrame("Home")
        else:
            messagebox.showerror("Error", "Thông tin đăng nhập không chính xác. Vui lòng thử lại.")
