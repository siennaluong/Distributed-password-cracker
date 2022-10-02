import socket
import threading
import hashlib
import time
import re
from tkinter import * 
from tkinter import ttk


HOST = '127.0.0.1'
PORT = 1234

message = ""

def communicate_to_server(client):
    global message
    while True:
        
        pswdHash = e1.get()
        print(pswdHash)
        if re.match("^[a-zA-Z0-9_]*$", pswdHash) and len(pswdHash) <= 8 and len(pswdHash) >= 4:
            pswdHash = hashlib.md5(pswdHash.encode())
            client.send(pswdHash.hexdigest().encode())
            break

        else:
           message ='Password did not fit the requirements.'

    message ='Correct password'
    
    message ='Waiting on response...\n'
    
    
    Label(root, text=pswdHash).pack()
    Label(root, text=message).pack()
    while True:
        data = client.recv(1024)
        if len(data) != 0:
            print(data.decode())
            message ="Program will automatically close in ten seconds."
            
            Label(root, text=message).pack()
            time.sleep(10)
            exit()



if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.send("1".encode())
    
    
    root = Tk()

    Label(root, text="Enter the password you wish to try: ").pack()
    e1 = Entry(root)
    e1.pack()
    
    Button(root, text="Let's crack it!", command=(lambda client=client: communicate_to_server(client))).pack()
    
    root.mainloop()
    

