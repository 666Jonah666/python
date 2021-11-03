import os, shutil
from settings import HOME_DIRECTORY
def fmanager():
    home_dir = HOME_DIRECTORY()
    while True:
        a = ["quit", "newfolder", "del", "to", "newfile", "same", "show", "send", "chpath"]
        user_input = input(f"{os.getcwd()}> ").split()
        if len(user_input) == 0:
            continue
        elif user_input[0] not in a:
            print(f'unknown command "{user_input[0]}"')
            continue
        else:
            if user_input[0] == "quit":
                print("exit from file manager...")
                break
            elif user_input[0] == "newfolder" and len(user_input) == 2:
                newfolder(user_input[1])
            elif user_input[0] == "del" and len(user_input) == 3:
                if user_input[1] == "-folder":
                    del_folder(user_input[2])
                elif user_input[1] == "-file":
                    del_file(user_input[2])
            elif user_input[0] == "to" and len(user_input) == 2:
                if user_input[1][:2:] == "./":
                    change_dir(os.getcwd() + user_input[1][1::], home_dir)
                elif user_input[1][0] == "/" or ":/" in user_input[1] or user_input[1] == "back":
                    change_dir(user_input[1], home_dir)
                else:
                    print("invalid input")
            elif user_input[0] == "newfile" and len(user_input) == 2:
                newfile(user_input[1])
            elif user_input[0] == "send" and len(user_input) > 1:
                if len(user_input[1:len(user_input)-1:]) == 0:
                     print('invalid input.\nyou need to input at least 2 arguments: send <text> <file name>')
                else:
                    send(user_input[1:len(user_input)-1:], user_input[len(user_input)-1])
            elif user_input[0] == "show" and len(user_input) == 2:
                show(user_input[1])
            elif user_input[0] == "same" and len(user_input) == 3:
                same(user_input[1], user_input[2], home_dir)
            elif user_input[0] == "chpath" and len(user_input) == 3:
                chpath(user_input[1], user_input[2], home_dir)
            else:
                print("invalid input")

def del_folder(f_name):
    current = os.getcwd()
    try:
        os.chdir(os.getcwd() + "/" + f_name)
    except FileNotFoundError:
        print(f'the folder "{f_name}" does not exist!')
    else:
        a = os.listdir()
        os.chdir(current)
        if len(a) != 0:
            while True:
                a = input(f'{f_name} have {len(a)} objects. Do you want to delete directory and all containing files? Type "y" or "n": ')
                if a == "y" or a == "":
                    shutil.rmtree(f_name)
                    print(f'directory "{f_name}" deleted with all files')
                    break
                elif a == "n":
                    break
                else:
                    print("invalid input")
        else:
            print(f'directory "{f_name}" deleted')
            os.rmdir(f_name)

def del_file(f_name):
    try:
        os.remove(f_name)
        print(f'file "{f_name}" has been removed')
    except FileNotFoundError:
        print(f'file "{f_name}" does not exist!')

def newfile(f_name):
    a = os.listdir()
    if f_name in a:
        print(f'file "{f_name}" already exist!')
    else:
        new_file = open(f_name, "w")
        new_file.close()
        print(f'the "{f_name}" file was created')

def same(f_name, destination, start):
    if (start not in destination) and ("\\" in destination):
        print("you cant exit outside the working folder")
    else:
        try:
            shutil.copy(f_name, destination)
        except FileNotFoundError:
            print('invalid input')
        except shutil.SameFileError:
            print(f'file "{f_name}" already exist')
        else:
            print(f'the file "{f_name}" was copied successfully ')


def show(f_name):
    a = os.listdir()
    if f_name not in a:
        print(f'file "{f_name}" does not exist!')
    else:
        with open(f_name) as file:
            print(''.join(file.readlines()))

def send(text, f_name):
    a = os.listdir()
    if f_name not in a:
        while True:
            ans = input(f'file "{f_name}" does not exist! Do you want to create a new file with this content? Type "y" or "n": ')
            if ans == "y" or ans == "":
                my_file = open(f_name, "w")
                my_file.write(' '.join(text))
                my_file.close()
                print(f'file "{f_name}" has been created with all content')
                break
            elif ans == "n":
                break
    else:
        my_file = open(f_name, "a")
        my_file.write(' '.join(text))
        my_file.close()
        print(f'text was sended to "{f_name}" file')

def chpath(f_name, destination, start):
    if "\\" in destination and start not in destination:
        print("you cant exit outside the working folder")
    else:
        try:
            shutil.move(f_name, destination)
        except FileNotFoundError:
            print("no such file or directory")
        else:
            if "\\" not in destination:
                print(f'file {f_name} successfully renamed to {destination}')
            else:
                print(f'file {f_name} successfully moved to {destination}')

def change_dir(f_name, start):
    if f_name == "back":
        a = os.getcwd()
        try:
            os.chdir('..')
        except:
            print('too far away')
        else:
            if start not in os.getcwd():
                print("you cant exit outside working folder")
                os.chdir(a)
            else:
                print(f'changing directory to: {os.getcwd()}')
    elif start in f_name:
        try:
            os.chdir(f_name)
        except FileNotFoundError:
            print(f'the folder "{f_name}" does not exist!')
        else:
            print(f'changing directory to: {os.getcwd()}')
    else:
        print('you cant exit outside working folder')

def newfolder(f_name):
    try:
        os.mkdir(f_name)
    except:
        print(f'folder "{f_name}" already exist!')

fmanager()
