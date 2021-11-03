import os

def HOME_DIRECTORY():
    directory = r"C:\Users\andre\Documents" #измените путь на желаемый для изменения домашней директории
    os.chdir(directory)
    return directory
