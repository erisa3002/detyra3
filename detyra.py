from socket import *
from threading import Thread
import tkinter, sys, time
import rsa


def receive():

    msg_list.insert(tkinter.END, " Welcome! %s" % NAME)
    msg_list.insert(tkinter.END, " You are online!")
    while True:
        try:
            msg = CLIENT.recv(BUFFER_SIZE).decode("utf8")
            msg = rsa.decrypt_string(msg, private_key_1)
            msg_list.insert(tkinter.END, msg)
        except OSError:
            break

def send(event = None):

    msg = my_msg.get()
    my_msg.set("")  
    msg = NAME + ": " + msg
    msg_list.insert(tkinter.END, msg)
    msg = rsa.encrypt_string(msg, public_key_2)
    CLIENT.send(bytes(msg, "utf8"))


def on_closing(event = None):
    msg_list.insert(tkinter.END, "going offline...")
    time.sleep(2)
    CLIENT.close()
    top.quit()
    sys.exit()



top = tkinter.Tk()
top.title("Entice")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar() 
my_msg.set("Type your messages..")
scrollbar = tkinter.Scrollbar(messages_frame)

msg_list = tkinter.Listbox(messages_frame, height=25, width=100, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text = "Send", command = send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)



HOST = input('Enter host: ')
PORT = int(input('Enter port: '))
NAME = input('Enter your name: ')
BUFFER_SIZE = 1024
ADDRESS = (HOST, PORT)

CLIENT = socket(AF_INET, SOCK_STREAM)
CLIENT.connect(ADDRESS)

public_key_1, private_key_1 = rsa.key_generator()
msg = str(public_key_1[0]) + '*' + str(public_key_1[1])
CLIENT.send(bytes(msg, "utf8"))
m = CLIENT.recv(BUFFER_SIZE).decode('utf8')
public_key_2 = [int(x) for x in m.split('*')]

receive_thread = Thread(target = receive)
receive_thread.start()
tkinter.mainloop()
