import tkinter as tk
import httprequests

LARGE_FONT= ("Verdana", 12)
refresh_token = None
access_token = None
username = "None"
class Main(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):

            frame = F(container, self)

            self.frames[F.__name__] = frame
            print (F.__name__)

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont.__name__]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        self.parent = parent
        label = tk.Label(self, text="Login", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        tk.Label(self,text="Login credetials",bg="white").pack()
        tk.Label(self,text="Email").pack()
        self.email = tk.StringVar()
        self.password = tk.StringVar()
        tk.Entry(self,textvariable=self.email).pack()
        tk.Label(self,text="Password").pack()
        tk.Entry(self,textvariable=self.password).pack()
        button = tk.Button(self, text="Login",
                           command=self.log_in)
        button.pack()
        button2 = tk.Button(self, text="Exit",command=exit)
        button2.pack()
        self.controller = controller
    def log_in(self):
        global access_token
        global refresh_token
        global username
        email = self.email.get()
        password = self.password.get()
        data = {"email":email, "password":password}
        request = httprequests.post_token(data)
        access_token = request["access_token"]
        refresh_token = request["refresh_token"]
        print(access_token)
        username = httprequests.get_me(access_token)["username"]
        app.frames[PageOne.__name__].update_name()
        self.controller.show_frame(PageOne)



class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        global username
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Home", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        self.text = tk.Label(self, text=username)
        self.text.pack()
        tk.Label(self,textvariable="yo").pack()
        tk.Listbox(self).pack()
        print("tekee page one")



        button2 = tk.Button(self, text="back",
                            command=lambda: controller.show_frame(StartPage))
        button2.pack()
    def update_name(self):
        global username
        print("gets called")
        self.text.config(text = username)


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



app = Main()
app.mainloop()