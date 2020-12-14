import tkinter as tk
import httprequests

LARGE_FONT= ("Verdana", 12)
refresh_token = None
access_token = None
item_list = []
class Main(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, CreateAccountPage, NewItemPage):

            frame = F(container, self)

            self.frames[F.__name__] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont.__name__]
        frame.tkraise()


class StartPage(tk.Frame): # log in screen

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        global access_token
        access_token = None

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
        self.text = tk.Label(self)
        self.text.pack()
        button = tk.Button(self, text="Login",
                           command=self.log_in)
        button.pack()
        button = tk.Button(self, text="Create account",
                           command=lambda: self.controller.show_frame(CreateAccountPage))
        button.pack()
        button3 = tk.Button(self, text="Login as guest", command=lambda:self.controller.show_frame(PageOne))
        button3.pack()
        button2 = tk.Button(self, text="Exit",command=exit)
        button2.pack(side=tk.BOTTOM)
        self.controller = controller
    def log_in(self):
        global access_token
        global refresh_token
        email = self.email.get()
        password = self.password.get()
        data = {"email":email, "password":password}
        request = httprequests.post_token(data)
        if "message" in request:
            self.text.config(text=request["message"])
        else:
            access_token = request["access_token"]
            refresh_token = request["refresh_token"]
            app.frames[PageOne.__name__].update_page()
            self.controller.show_frame(PageOne)



class PageOne(tk.Frame): # homepage

    def __init__(self, parent, controller):
        global access_token
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Home", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        self.welcome = tk.Label(self, text="Welcome User")
        self.welcome.pack()
        self.username_search = tk.StringVar()
        self.item_search = tk.StringVar()
        button = tk.Button(self, text="Search item", command=self.search_item)
        button.pack()
        tk.Entry(self, textvariable=self.item_search).pack()
        button = tk.Button(self, text="Search user", command=self.search_user)
        button.pack()
        tk.Entry(self, textvariable=self.username_search).pack()
        self.feedback = tk.Label(self)
        self.feedback.pack()
        self.my_items_button = tk.Button(self, text="My items", command=self.my_items)
        self.new_item = tk.Button(self, text="New item", command=lambda: self.controller.show_frame(NewItemPage))
        button2 = tk.Button(self, text="back",
                            command=lambda: controller.show_frame(StartPage))
        button2.pack(side=tk.BOTTOM)

    def search_item(self):
        global item_list
        item_list = []
        tag = self.item_search.get()
        request = httprequests.search_items(tag)
        if not ("message" in request):
            item_list.append(request["data"][0])
        request2 = httprequests.search_items_name(tag)
        if not("message" in request2):
            item_list.append(request2["data"][0])
        print(item_list)
        app.frames[PageTwo.__name__].update_page()
        self.controller.show_frame(PageTwo)
    def search_user(self):
        global access_token
        if access_token:
            user = httprequests.get_user(self.username_search.get(), access_token)
        else:
            user = httprequests.get_user_unregistered(self.username_search.get())
        if "message" in user:
            self.feedback.config(text=user["message"])
        if "email" in user:
            self.feedback.config(text=user["username"] + ": id : "+ str(user["id"]) + ": email " + str(user["email"]))
        else:
            self.feedback.config(text=user["username"] + ": id : " + str(user["id"]))

    def my_items(self):
        global access_token
        global item_list
        username = httprequests.get_me(access_token)["username"]
        request = httprequests.get_all_by_user(username)
        if "message" in request:
            return
        else:
            item_list = request["data"]
            app.frames[PageTwo.__name__].update_page()
            self.controller.show_frame(PageTwo)


    def update_page(self):
        global access_token
        if access_token:
            username = httprequests.get_me(access_token)["username"]
            self.welcome.config(text = "Welcome "+username)
            self.my_items_button.pack()
            self.new_item.pack()


class PageTwo(tk.Frame): # items page

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Items", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        self.controller = controller
        self.item_index = 0
        self.name = tk.Label(self, text="")
        self.description = tk.Label(self, text="")
        self.rating = tk.Label(self, text="")
        self.author = tk.Label(self, text="")
        self.amount = tk.Label(self, text="")
        self.price = tk.Label(self, text="")
        self.name.pack()
        self.description.pack()
        self.rating.pack()
        self.author.pack()
        self.amount.pack()
        self.price.pack()
        self.button_next = tk.Button(self, text="Next item", command=lambda: self.change_item(1))
        self.button_previous = tk.Button(self, text="Previous item", command=lambda: self.change_item(-1))
        self.button_next.pack()
        self.button_previous.pack()
        self.update_item = tk.Button(self, text="Update Item",
                                     command=lambda: self.controller.show_frame(NewItemPage))


        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageOne))
        button1.pack(side=tk.BOTTOM)

    def update_page(self):
        global item_list
        global access_token
        if self.item_index > len(item_list)-1:
            self.item_index = 0
        item = item_list[self.item_index]
        self.name.config(text="Name: "+str(item["name"]))
        self.description.config(text="Description: "+str(item["description"]))
        self.rating.config(text="Rating: "+str(item["rating"]))
        self.author.config(text="Author: "+str(item["author"]["username"]))
        self.price.config(text="Price: "+str(item["price"]))
        self.amount.config(text="Amount: "+str(item["amount"]))
        if access_token:
            if str(httprequests.get_me(access_token)["id"]) == str(item["author"]["id"]):
                self.update_item.pack()
            else:
                self.update_item.pack_forget()

    def change_item(self, n):
        global item_list
        self.item_index += n
        if self.item_index < 0:
            self.item_index = len(item_list) -1
        if self.item_index > len(item_list)-1:
            self.item_index = 0
        self.update_page()

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
        button = tk.Button(self, text="BacK", command=lambda: self.controller.show_frame(StartPage))
        button.pack(side=tk.BOTTOM)

    def create_account(self):
        data = {"username":self.username.get(), "email":self.email.get(), "password":self.password.get()}
        request = httprequests.post_user(data)
        if "message" in request:
            self.feedback.config(text = request["message"])
        else:
            self.feedback.config(text = "Account created!")

class NewItemPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.name = tk.StringVar()
        self.name_entry = tk.Entry(self, textvariable=self.name)
        self.description = tk.StringVar()
        self.description_entry = tk.Entry(self, textvariable=self.description)
        self.price = tk.IntVar()
        self.price_entry = tk.Entry(self, textvariable=self.price)
        self.amount = tk.IntVar()
        self.amount_entry = tk.Entry(self, textvariable=self.amount)
        self.tag1 = tk.StringVar()
        self.tag1_entry = tk.Entry(self, textvariable=self.tag1)
        self.tag2 = tk.StringVar()
        self.tag2_entry = tk.Entry(self, textvariable=self.tag2)
        self.tag3 = tk.StringVar()
        self.tag3_entry = tk.Entry(self, textvariable=self.tag3)

        tk.Label(self, text="Item name").pack()
        self.name_entry.pack()
        tk.Label(self, text="Item description").pack()
        self.description_entry.pack()
        tk.Label(self, text="Item price").pack()
        self.price_entry.pack()
        tk.Label(self, text="Amount of items").pack()
        self.amount_entry.pack()
        tk.Label(self, text="Tags for finding your item").pack()
        self.tag1_entry.pack()
        self.tag2_entry.pack()
        self.tag3_entry.pack()
        button = tk.Button(self, text="Create Item", command=self.create_item)
        button.pack()
        self.feedback = tk.Label(self, text="")
        self.feedback.pack()

    def create_item(self):
        global access_token
        data = {"name":str(self.name.get()),
                "description":str(self.description.get()),
                "price":int(self.price.get()),
                "amount":int(self.amount.get()),
                "tag1":str(self.tag1_entry.get()),
                "tag2":str(self.tag2_entry.get()),
                "tag3":str(self.tag3_entry.get())}
        request = httprequests.post_item(data, access_token)
        if "message" in request:
            self.feedback.config(text=str(request["message"]))
        else:
            self.controller.show_frame(PageOne)




app = Main()
app.mainloop()