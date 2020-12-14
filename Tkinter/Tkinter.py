import tkinter as tk
import httprequests

LARGE_FONT= ("Verdana", 12)
refresh_token = None
access_token = None
class Main(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, CreateAccountPage):

            frame = F(container, self)

            self.frames[F.__name__] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont.__name__]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        self.parent = parent
        self.controller = controller
        label = tk.Label(self, text="Login", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        tk.Label(self,text="Login credentials",bg="white").pack()
        tk.Label(self,text="Email").pack()
        self.email = tk.StringVar()
        self.password = tk.StringVar()
        tk.Entry(self,textvariable=self.email).pack()
        tk.Label(self,text="Password").pack()
        tk.Entry(self,textvariable=self.password).pack()
        button = tk.Button(self, text="Login",
                           command=self.log_in)
        button.pack()
        button = tk.Button(self, text="Create account",
                           command=lambda: self.controller.show_frame(CreateAccountPage))
        button.pack()
        button2 = tk.Button(self, text="Exit",command=exit)
        button2.pack()
        self.controller = controller
    def log_in(self):
        global access_token
        global refresh_token
        email = self.email.get()
        password = self.password.get()
        data = {"email":email, "password":password}
        request = httprequests.post_token(data)
        access_token = request["access_token"]
        refresh_token = request["refresh_token"]
        app.frames[PageOne.__name__].update_name()
        self.controller.show_frame(PageOne)



class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Home", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        self.text = tk.Label(self, text="")
        self.text.pack()
        tk.Label(self,textvariable="yo").pack()
        tk.Listbox(self).pack()



        button2 = tk.Button(self, text="back",
                            command=lambda: controller.show_frame(StartPage))
        button2.pack()
    def update_name(self):
        username = httprequests.get_me(access_token)["username"]
        self.text.config(text = "Welcome "+username)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()

class CreateAccountPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.email = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        label = tk.Label(self, text="Username")
        label.pack()
        tk.Entry(self, textvariable=self.username).pack()
        label2 = tk.Label(self, text="Email")
        label2.pack()
        tk.Entry(self, textvariable=self.email).pack()
        label3 = tk.Label(self, text="Password")
        label3.pack()
        tk.Entry(self, textvariable=self.password).pack()
        button = tk.Button(self, text = "Create account", command=self.create_account)
        button.pack()
        self.feedback = tk.Label(self)
        self.feedback.pack()
        button = tk.Button(self, command=lambda: self.controller.show_frame(StartPage))
        button.pack()

    def create_account(self):
        data = {"username":self.username.get(), "email":self.email.get(), "password":self.password.get()}
        request = httprequests.post_user(data)
        if "message" in request:
            self.feedback.config(text = request["message"])
        else:
            self.feedback.config(text = "Account created!")




app = Main()
app.mainloop()