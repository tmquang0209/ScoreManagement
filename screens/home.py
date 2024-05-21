import json
from tkinter import Frame, Label, Button, ttk
from tkinter import messagebox
import modules.localStorage as localStorage

class Home(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.controller.config(menu=None)

        self.userName = ""

        # Welcome label
        self.welcomeLabel = Label(self, text="Welcome, " + self.userName, font=("Helvetica", 18))
        self.welcomeLabel.pack(side="top", fill="x", pady=10)
        self.prepareHome()

        # Logout button
        logoutButton = ttk.Button(self, text="Logout", command=self.logout)
        logoutButton.pack()

    def fetchUserInfo(self):
        userData = localStorage.getItem("user")
        userData = json.loads(userData) if userData else None

        if userData:
            self.welcomeLabel.config(text="Welcome, " + userData["name"])

    def updateMenu(self):
        from modules.menu import MenuManager
        menuManager = MenuManager(self.controller)
        menu = menuManager.createMenu()
        self.controller.config(menu=menu)

    def prepareHome(self):
        self.fetchUserInfo()
        self.updateMenu()

    def logout(self):
        # Confirm logout dialog
        confirmation = messagebox.askquestion("Xác nhận thoát", "Bạn có chắc chắn muốn thoát không?")
        if confirmation == "yes":
            localStorage.clear()
            self.controller.title("Đăng nhập")
            self.controller.config(menu=None)
            self.controller.showFrame("Login")
