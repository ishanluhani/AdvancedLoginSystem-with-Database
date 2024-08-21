import customtkinter as ctk
import LoginPage
import dashboardPage

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.user = ''

        # Defining Layout
        self.geometry('500x430')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.tabViewer = LoginPage.LoginSignupPage(self)
        self.tabViewer.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

    def notifyLogin(self, user):
        print('Welcome Abroad')

        self.user = user
        self.geometry('750x700')

        self.dashboard = dashboardPage.Dashboard(self, self.user)
        self.dashboard.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

    def notifyLogout(self):
        self.dashboard.destroy()
        self.geometry('500x430')

        self.tabViewer = LoginPage.LoginSignupPage(self)
        self.tabViewer.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

if __name__ == '__main__':
    app = App()
    app.mainloop()

