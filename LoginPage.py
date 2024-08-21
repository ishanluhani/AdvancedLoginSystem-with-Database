import re
import customtkinter as ctk
import backendDatabaseManagement
from backendExtras import *


# This class helps transmit Login Message
class CustomCtkFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

    def notifyLogin(self, user):
        self.master.notifyLogin(user)


class LoginSignupPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='transparent')
        self.modes = ['Signup', 'Login']

        # Defining Layout
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.rowconfigure(0, weight=1)

        # Defining Widgets
        self.widgetFrame = CustomCtkFrame(self)
        self.chooseButton = ctk.CTkSegmentedButton(self.widgetFrame, values=self.modes, command=self.changeMode)
        self.signupFrame = SignupFrame(self.widgetFrame)
        self.loginFrame = LoginFrame(self.widgetFrame)

        # Configuring Widgets
        self.widgetFrame.columnconfigure((0, 1, 2), weight=1)
        self.widgetFrame.rowconfigure(1, weight=1)

        self.chooseButton.set('Signup')

        # Placing Widgets
        self.widgetFrame.grid(row=0, column=1, columnspan=6, pady=(5, 10), sticky='nsew')
        self.chooseButton.grid(row=0, column=1, padx=20, sticky='ew')
        self.signupFrame.grid(row=1, column=0, columnspan=3, pady=(5, 10), sticky='nsew')

    def changeMode(self, value):
        if value == 'Signup':
            self.loginFrame.destroy()
            self.signupFrame.grid(row=1, column=0, columnspan=3, pady=(5, 10), sticky='nsew')
            self.loginFrame = LoginFrame(self.widgetFrame)
        else:
            self.signupFrame.destroy()
            self.loginFrame.grid(row=1, column=0, columnspan=3, pady=(5, 10), sticky='nsew')
            self.signupFrame = SignupFrame(self.widgetFrame)

    def notifyLogin(self, user):
        self.master.notifyLogin(user)


class SignupFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='transparent')

        # Defining Layout
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        self.columnconfigure(0, weight=1)
        self.grid_propagate(False)  # freezes resizing of Frame (self)

        # Adding Widgets
        self.emailWidget = self.addEntry('Enter your Email ID', 0)
        self.passwordWidget = self.addEntry('Enter your Password', 2, isPassword=True)
        self.cpasswordWidget = self.addEntry('Confirm your Password', 4, isPassword=True)

        self.submitButton = ctk.CTkButton(self, text='Create Account', command=self.validify)
        self.submitButton.grid(row=7, column=0, sticky='nsew')

        self.infoLabel = ctk.CTkLabel(self, text='', text_color='red')
        self.infoLabel.grid(row=9, column=0, sticky='nsew')

    def addEntry(self, text, row, isPassword=False):
        # Creates a basic Entry with a Label
        ctk.CTkLabel(self, text=text).grid(row=row, column=0, padx=7, sticky='sw')
        widget = ctk.CTkEntry(self, font=('sans-serif', 18))
        widget.grid(row=row+1, column=0, sticky='nsew', padx=7)

        if isPassword:
            widget.configure(show='*')

        return widget

    def validify(self):
        # Defining Local Variables
        emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        email = self.emailWidget.get()
        password = self.passwordWidget.get()
        cpassword = self.cpasswordWidget.get()

        # Validating the Filled Content (Email, Password)
        if (not email) or (not password) or (not cpassword):
            self.infoLabel.configure(text='Please Fill all the Fields')

        elif not re.fullmatch(emailRegex, email):
            self.infoLabel.configure(text='Please Enter a valid Email ID')

        elif password != cpassword:
            self.passwordWidget.delete(0, ctk.END)
            self.cpasswordWidget.delete(0, ctk.END)
            self.infoLabel.configure(text='Password does not match')

        elif len(password) < 8:
            self.passwordWidget.delete(0, ctk.END)
            self.cpasswordWidget.delete(0, ctk.END)
            self.infoLabel.configure(text='Length of Password must be at least 8')

        elif backendDatabaseManagement.checkUserExists(email):
            self.infoLabel.configure(text='This Email already exists, Please Login to Continue')

        else:
            # Verifying Email by OTP
            otp = sendVerificationOTP(email)
            verifyPrompt = ctk.CTkInputDialog(text="Enter the verification OTP sent to you via Email:",
                                              title="Enter OTP")

            if verifyPrompt.get_input() != otp:
                self.infoLabel.configure(text='Please Enter Correct OTP')
            else:
                print('Identity confirmed')
                user = backendDatabaseManagement.addUser(self.emailWidget.get(), self.passwordWidget.get())
                self.master.notifyLogin(user)

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='transparent')

        # Defining Layout
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        self.columnconfigure(0, weight=1)
        self.grid_propagate(False)  # freezes resizing of Frame (self)

        # Adding Widgets
        self.emailWidget = self.addEntry('Enter your Email ID', 0)
        self.passwordWidget = self.addEntry('Enter your Password', 2, isPassword=True)

        self.submitButton = ctk.CTkButton(self, text='Login', command=self.loginUser)
        self.submitButton.grid(row=7, column=0, sticky='nsew')

        self.infoLabel = ctk.CTkLabel(self, text='', text_color='red')
        self.infoLabel.grid(row=9, column=0, sticky='nsew')

    def addEntry(self, text, row, isPassword=False):
        # Creates a basic Entry with a Label
        ctk.CTkLabel(self, text=text).grid(row=row, column=0, padx=7, sticky='sw')
        widget = ctk.CTkEntry(self, font=('sans-serif', 18))
        widget.grid(row=row + 1, column=0, sticky='nsew', padx=7)

        if isPassword:
            widget.configure(show='*')

        return widget

    def loginUser(self):
        email = self.emailWidget.get().lower()
        password = self.passwordWidget.get()

        self.user = backendDatabaseManagement.loginUser(email, password)
        if self.user:
            self.master.notifyLogin(self.user)
        else:
            self.infoLabel.configure(text='Please Enter Correct Email ID or Password')
