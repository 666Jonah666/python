from tkinter import *
from tkinter.ttk import *
from tkcalendar import Calendar, DateEntry #required to install
from tkinter import messagebox
import ast

master = Tk()
master.title("sign in")
master.geometry("300x150")

def signin(usname, passwd): #sign in function
    #check if user with that username exist and password is correct
    objects = []
    inputFile = open( "myDicts.txt", "r")
    lines = inputFile.readlines()
    exist = False
    for line in lines:
        objects.append( ast.literal_eval(line) )
    for i in objects:
        if i['username'] == usname.get() and i['passw'] == passwd.get():
            exist = True
    if exist == False:
        messagebox.showerror('error', 'Неверное имя пользователя или пароль')
    else: #if user signed in successfully print hello message
        messagebox.showinfo('Hello!', f'Авторизация успешна\nПривет {usname.get()}!')

def check_if_data_match(passw1,pass2, uname, birth, g, group_n, window):
    #recieved data from vars
    passw = passw1.get()
    passw2 = pass2.get()
    b_date = birth.get()
    username = uname.get()
    group = group_n.get()

    #check data
    if len(uname.get()) == 0 or g.get() == 0: #check that username and gender is selected
        messagebox.showerror('error', 'Заполните все поля')
    elif int(birth.get()[len(birth.get()) - 4::]) > 2004: #check if the user is 18y old
        messagebox.showerror('error', 'вам должно быть 18 лет')
    elif passw != passw2: #checking that password1 and password2 are equal
        messagebox.showerror('error', 'Пароли не совпадают')
    else:
        #create dict from entries
        gender = ('male' if g.get() == 1 else 'female')
        data = dict()
        for variable in ["username", "passw", "b_date", "gender", "group"]:
            data[variable] = eval(variable)

        #check if user with that username is already exist
        objects = []
        inputFile = open( "myDicts.txt", "r")
        lines = inputFile.readlines()
        new = True
        for line in lines:
            objects.append( ast.literal_eval(line) )
        for i in objects:
            if i['username'] == username:
                messagebox.showerror('error', f'пользователь с ником {username} уже существует')
                new = False

        #if user does not exist write dictionary to file
        if new:
            outputFile = open( "myDicts.txt", "a")
            outputFile.write(str(data))
            outputFile.write('\n')
            outputFile.flush()
            outputFile.close()
            if messagebox.showinfo("Success", "Пользователь создан. Теперь вы можете войти"): #return user to first window
                window.destroy()

def openNewWindow(): #sign up function
    #create new window
    newWindow = Toplevel(master)
    newWindow.title("sign up")
    newWindow.geometry("400x300")

    #username entry
    Label(newWindow,text ="Username: ").place(x=80,y=10)
    uname = StringVar()
    e1 = Entry(newWindow, textvariable=uname).place(x=200,y=10)

    #password entry
    Label(newWindow,text ="password").place(x=80,y=50)
    p1 = StringVar()
    e2 = Entry(newWindow, textvariable=p1, show='*').place(x=200,y=50)
    Label(newWindow, text ="repeat password").place(x=80,y=90)
    p2 = StringVar()
    e3 = Entry(newWindow, textvariable=p2, show='*').place(x=200,y=90)

    #date entry
    Label(newWindow,text ="Date of Birth").place(x=80,y=130)
    cal_s = StringVar()
    cal = DateEntry(newWindow, textvariable=cal_s, foreground='white', date_pattern='mm/dd/y').place(width=90, x=200,y=130)

    #radio buttons
    gender = IntVar(newWindow)
    gender.set(0)
    male = Radiobutton(newWindow, text="male",variable=gender, value=1).place(x=80,y=170)
    female = Radiobutton(newWindow, text="female",variable=gender, value=2).place(x=200,y=170)

    #select group from list
    Label(newWindow,text ="select group").place(x=80,y=210)
    group = StringVar(newWindow)
    group.set("PI20-1")
    list = OptionMenu(newWindow, group, "PI20-1", "PI20-1", "PI20-2", "PI20-3").place(x=200,y=210)

    #confirm sign up button
    btn = Button(newWindow, text ="SignUp", command=lambda: check_if_data_match(p1, p2, uname, cal_s, gender, group, newWindow)).place(x=140,y=250)

#username entry
label = Label(master, text ="Username").place(x=45,y=20)
usname = StringVar()
nick = Entry(master, textvariable=usname).place(x=115,y=20)

#password entry
Label(master,text ="Password").place(x=45,y=60)
password = StringVar()
passwd = Entry(master, textvariable=password, show='*').place(x=115,y=60)

#sign in sign up buttons
btn1 = Button(master, text ="sign in", command = lambda: signin(usname, password)).place(x=55,y=100)
btn2 = Button(master, text ="sign up", command = openNewWindow).place(x=165,y=100)

# mainloop runs infinitely
mainloop()
