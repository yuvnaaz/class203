import socket
from threading import Thread
from tkinter import *
#nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))

print("Connected with the server...")

class GUI:
    def __init__(self):
        self.window = Tk()
        self.window.withdraw()
        self.login = Toplevel()
        self.login.title("Login")
        self.login.geometry("400x400")
        self.login.resizable(width = False, height = False)
        self.head = Label(self.login, text = "please login to continue", justify = CENTER, font = "Calibri 20 bold")
        self.head.place(relheight = 0.15, relx = 0.2, rely = 0.07)
        self.label_name = Label(self.login, text = "Name", font = "Helvetica 14")
        self.label_name.place(relheight = 0.2, relx = 0.1, rely = 0.17)
        self.entry_name = Entry(self.login, font = "Calibri 14")
        self.entry_name.place(relwidth = 0.4, relheight = 0.12, relx = 0.35, rely = 0.2)
        self.entry_name.focus()
        self.go = Button(self.login, text = "Continue", font = "Helvetica 14 bold", command = lambda: self.goAhead(self.entry_name.get()))
        self.go.place(relx = 0.4, rely = 0.55)
        self.window.mainloop()
    def goAhead(self,name):
        self.login.destroy()
        self.layout(name) 
        thread1 = Thread(target = self.receive)
        thread1.start()
    def layout(self,name):
        self.name = name
        self.window.deiconify()
        self.window.title("Chatroom")
        self.window.resizable(width = False, height = False)
        self.window.configure(width = 470, height = 550, bg = "#17202A")
        self.labelHead = Label(self.window, text = self.name, bg = "#17202A", fg = "#EAECEE", font = "Helvetica 13 bold", pady = 5)
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.window, width = 450, bg = "#ABB2B9")
        self.line.place(relwidth = 1, rely = 0.07, relheight = 0.012)
        self.textArea = Text(self.window, width = 20, height = 2, bg = "#17202A", fg = "#EAECEE", font = "Helvetica 14", padx = 5, pady = 5 )
        self.textArea.place(relheight = 0.745, relwidth = 1, rely = 0.08)
        scrollBar = Scrollbar(self.textArea)
        scrollBar.place(relheight = 1, relx = 0.974)
        scrollBar.config(command = self.textArea.yview)
        self.textArea.config(state = DISABLED)
        self.entryMsg = Entry(self.window, bg = "#2c3e50", fg = "#eaecee", font = "Helvetica 13")
        self.entryMsg.place(relwidth = 0.74, relheight = 0.1, rely = 0.85, relx = 0.01)
        
        self.buttonMsg = Button(self.window, text = "send", font ="Helvetica 13", width = 20, bg = "#ABB2B9", command = lambda: self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(relwidth = 0.22, relheight = 0.1, rely = 0.85, relx = 0.78)
    def sendButton(self, msg):
        self.textArea.config(state = DISABLED)
        self.msg = msg
        self.entryMsg.delete(0,END)
        thread1 = Thread(target = self.write)
        thread1.start()
    def write(self):
        self.textArea.config(state = DISABLED)
        while True:
            message = '{}: {}'.format(self.name, self.msg)
            client.send(message.encode('utf-8'))
            self.showMessage(message)
            break


    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message == 'NICKNAME':
                    client.send(nickname.encode('utf-8'))
                else:
                    self.showMessage(message)
            except:
                print("An error occured!")
                client.close()
                break
    def showMessage(self,message):
        self.textArea.config(state = NORMAL)
        self.textArea.insert(END, messgae+"\n")
        self.textArea.config(state = DISABLED)
        self.textArea.see(END)
        
g = GUI()





# receive_thread = Thread(target=receive)
# receive_thread.start()
# write_thread = Thread(target=write)
# write_thread.start()
