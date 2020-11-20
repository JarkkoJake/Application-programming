from tkinter import *
Login = Tk()
Login.geometry("500x300")
Login.title("Login")
Label(text="login credetials",width="100",height="5",bg="white").pack()

def Main():
    Mainmenu = Toplevel(Login)
    Mainmenu.title("Home")
    Mainmenu.geometry("600x400")


usernameLabel= Label(text="Username").pack()
username = StringVar()
usernameEntry =Entry (Login,textvariable=username).pack()


passwordLabel= Label(text="password").pack()
password = StringVar()
passwordEntry = Entry(Login,textvariable=password).pack()
Label(Login,text="").pack()
button = Button(Login,text="login",width=10,command=Main ,bg="red").pack(pady=0)
button1 = Button(Login,text="exit",width=10,command=exit,bg="red").pack(pady=0)



def exit():
    Login.destroy()
    exit()

Login.mainloop()