from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tkt

server_closed = False  

def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkt.END,msg)
        except OSError:  
            break
        
        
def send(event=None):
        msg = my_msg.get()
        my_msg.set("")
        try:
            client_socket.send(bytes(msg, "utf8"))
        except ConnectionResetError:
            print("Server has closed.")
            window.after(1000,window.destroy)
        if msg == "{quit}":
            client_socket.close()
            window.quit()
         
      
def on_closing():
    global server_closed
    if not server_closed:
        try:
            client_socket.send(bytes("{quit}", "utf8"))
        except Exception as e:
            print(f"Error while closing client: {str(e)}")
    window.destroy()
    
    
#GUI

window = tkt.Tk()
window.title("Project_Chat")


messages_frame = tkt.Frame(window)
my_msg = tkt.StringVar()
scrollbar = tkt.Scrollbar(messages_frame)

msg_list = tkt.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
msg_list.pack(side=tkt.LEFT, fill=tkt.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkt.Entry(window, textvariable=my_msg)
entry_field.bind("<Return>", send)

entry_field.pack()
send_button = tkt.Button(window, text="Invio", command=send)
send_button.pack()

window.protocol("WM_DELETE_WINDOW", on_closing)





HOST = input('Enter Server host: ')
PORT = input("Enter Server host's port: ")
if not PORT:
    PORT = 2003
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()

tkt.mainloop()


