from PIL import Image
import customtkinter as ctk
import LoginPage


class Dashboard(ctk.CTkFrame):
    def __init__(self, master, userData):
        # Initializing variables
        super().__init__(master)
        self.userData = userData

        # Defining Layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=100)

        self.header = DashboardHeader(self, text='My Dashboard')
        self.body = DashboardBody(self, self.userData)

        self.header.grid(row=0, column=0, sticky='nsew', padx=7, pady=7)
        self.body.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=7, pady=7)

    def clickSubject(self, name):

        self.header.destroy()
        self.header = SubjectHeader(self, text=name)
        self.header.grid(row=0, column=0, sticky='nsew', padx=7, pady=7)

        self.body.destroy()
        subjectData = self.userData['Subjects'][name]
        self.body = SubjectBody(self, subjectData)
        self.body.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=7, pady=7)

    def notifyLogout(self):
        self.master.notifyLogout()

    def notifyBack(self):
        self.header = DashboardHeader(self, text='My Dashboard')
        self.body = DashboardBody(self, self.userData)

        self.header.grid(row=0, column=0, sticky='nsew', padx=7, pady=7)
        self.body.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=7, pady=7)


class DashboardBody(ctk.CTkFrame):
    def __init__(self, master, userData):
        super().__init__(master)
        self.configure(fg_color='transparent')
        self.userData = userData

        # Defining Layout
        self.rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.columnconfigure(0, weight=1)

        self.userSubjects = self.userData['Subjects'].keys()
        for index, subject in enumerate(self.userSubjects):
            self.clickSubject(index, subject)


    def clickSubject(self, rowNo, subject):
        headingFont = ctk.CTkFont(family='Arial', size=32, weight='bold')
        icon = ctk.CTkImage(Image.open(f'assets/{subject}.png'), size=(90, 90))
        click = lambda: self.master.clickSubject(subject)
        widget = ctk.CTkButton(self, text=f' {subject}', font=headingFont, anchor='w', image=icon, compound='left', hover_color='gray20', corner_radius=25, command=click)
        widget.configure(fg_color='gray25')
        widget.grid(row=rowNo, column=0, padx=10, pady=(15, 0), sticky='nsew')


class SubjectBody(ctk.CTkScrollableFrame):
    def __init__(self, master, subjectData):
        super().__init__(master)
        self.configure(fg_color='transparent')

        self.subjectData = subjectData
        self.workTitle = list(self.subjectData.keys())

        self.rowconfigure(list(range(len(self.workTitle))), weight=1, minsize=95)
        self.columnconfigure(0, weight=1)


        self.workStatus = []
        for work in self.subjectData:
            status = self.subjectData[work]['Status']
            self.workStatus.append(status)
        self.workPackage = list(zip(self.workTitle, self.workStatus))
        print(self.workPackage)

        for index, (title, status) in enumerate(self.workPackage):
            headingFont = ctk.CTkFont(family='Arial', size=26, weight='bold')
            icon = ctk.CTkImage(Image.open(f'assets/{status}.png'), size=(20*4, 7*4))
            print(icon.cget('size'))
            iconLabel = ctk.CTkLabel(self, text='Checked')
            iconLabel.configure(fg_color='green')
            widget = ctk.CTkButton(self, text='CTkButton                                                           ', anchor='w', hover_color='gray20', image=icon, font=headingFont, corner_radius=10, compound='right')
            widget.configure(fg_color='gray25')

            iconLabel.grid(row=index, column=0, padx=10, pady=(20, 0), sticky='nsew')
            widget.grid(row=index, column=0, padx=10, pady=(20, 0), sticky='nsew')


class SubjectHeader(ctk.CTkFrame):
    def __init__(self, master, text):
        super().__init__(master)

        # Defining Layout
        self.columnconfigure(0, weight=10)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)

        # Defining Widgets
        self.textFrame = HeaderTextFrame(self, text)
        self.buttonFrame = SubjectButtonFrame(self)

        # Placing Widgets
        self.textFrame.grid(row=0, column=0, pady=20, sticky='nsew')
        self.buttonFrame.grid(row=0, column=1, sticky='nsew')

    def notifyBack(self):
        self.master.notifyBack()


class SubjectButtonFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='transparent')

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.headingButton = ctk.CTkButton(self, fg_color='red', text='Go Back', text_color='white', hover_color='darkred', command=self.notifyBack)
        self.headingButton.grid(row=0, column=1, pady=20, padx=20, sticky='nse')

    def notifyBack(self):
        self.master.notifyBack()


class DashboardHeader(ctk.CTkFrame):
    def __init__(self, master, text):
        super().__init__(master)

        # Defining Layout
        self.columnconfigure(0, weight=10)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)

        # Defining Widgets
        self.textFrame = HeaderTextFrame(self, text)
        self.buttonFrame = HeadingButtonFrame(self)

        # Placing Widgets
        self.textFrame.grid(row=0, column=0, pady=20, sticky='nsew')
        self.buttonFrame.grid(row=0, column=1, sticky='nsew')

    def notifyLogout(self):
        self.master.notifyLogout()


class HeadingButtonFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='transparent')

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.headingButton = ctk.CTkButton(self, fg_color='red', text='Logout', text_color='white', hover_color='darkred', command=self.notifyLogout)
        self.headingButton.grid(row=0, column=1, pady=20, padx=20, sticky='nse')

    def notifyLogout(self):
        self.master.notifyLogout()


class HeaderTextFrame(ctk.CTkFrame):
    def __init__(self, master, text):
        super().__init__(master)

        self.configure(fg_color='transparent')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.headingFont = ctk.CTkFont(family='Arial', size=40, weight='bold')
        self.headingText = ctk.CTkLabel(self, text=text, font=self.headingFont)
        self.headingText.grid(row=0, column=0, padx=(20, 0), sticky='wns')

