import socket
import threading
import time
import sys
import os

from tkinter import *



IP = '127.0.0.1'
PORT = 1234
LISTENER_LIMIT = 10



def client_handler(s):
    global passHash
    passHash = (s.recv(2048).decode())
    print('Provided hash is: ' + passHash)

def worker_result(client_worker, requesters, workers):
    while True:
        response = client_worker.recv(1024).decode()


        if len(response) != 0:
            response = ('Password found! ' + response)
            print(response)
            print('Succesful crack, server will restart in ten seconds.')
            requesters[0].send(response.encode())
            time.sleep(10)

            for connection in workers:
                connection.close()

            os.execl(sys.executable, sys.executable, *sys.argv)

def worker_handler(client_worker, workers, requesters):
    global passHash
    while True:
        sendHash = ""
        if len(requesters) == 1:
            if passHash != "":
                sendHash = passHash
                client_worker.send(sendHash.encode())                   
            if len(workers) == 1:
                time.sleep(0.1)
                parameters = "45678"
                workers[0].send(parameters.encode())
                if sendHash != "":
                    break
            elif len(workers) == 2:
                time.sleep(0.1)
                parameters = "48"
                workers[0].send(parameters.encode())
                time.sleep(0.1)
                parameters = "567"
                workers[1].send(parameters.encode())
                if sendHash != "":
                    break
            elif len(workers) == 3:
                parameters = "45"
                workers[0].send(parameters.encode())
                time.sleep(0.1)
                parameters = "67"
                workers[1].send(parameters.encode())
                time.sleep(0.1)
                parameters = "8"
                workers[2].send(parameters.encode())
                if sendHash != "":
                    break
            elif len(workers) == 4:
                parameters = "45"
                workers[0].send(parameters.encode())
                time.sleep(0.1)
                parameters = "6"
                workers[1].send(parameters.encode())
                time.sleep(0.1)
                parameters = "7"
                workers[2].send(parameters.encode())
                time.sleep(0.1)
                parameters = "8"
                workers[3].send(parameters.encode())
                if sendHash != "":
                    break
            elif len(workers) == 5:
                parameters = "4"
                workers[0].send(parameters.encode())
                time.sleep(0.1)
                parameters = "5"
                workers[1].send(parameters.encode())
                time.sleep(0.1)
                parameters = "6"
                workers[2].send(parameters.encode())
                time.sleep(0.1)
                parameters = "7"
                workers[3].send(parameters.encode())
                time.sleep(0.1)
                parameters = "8"
                workers[4].send(parameters.encode())
                if sendHash != "":
                    break
            
            
    

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP, PORT))
    s.listen(LISTENER_LIMIT)
    print('The server is waiting on clients...')
    workers = list()
    workerHandlers = list()
    requesters = list()
    requester = 0
    passHash = ""
    hashs = list()
    hashs.append(passHash)
    while True:
        client, addr = s.accept()

        print('Connection recieved from: ', addr)
        queryResponse = client.recv(1024).decode()

        if queryResponse == "1":

          
            if len(requesters) == 0:
                print(addr, " Is a requester.")
                reqThread = threading.Thread(
                    target= client_handler, args=(client,), daemon=True)
                reqThread.start()
                requesters.append(client)

          
            else:
                message = "Currently handling a different request, could not connect this request."
                client.send(message.encode())
                client.close()

        elif queryResponse == "2":

            if len(workers) == 6:
                message = "Worker overload, too many attempted connect, server restarting."
                client.send(message.encode())
                print(message)
                client.close()

            else:
                print(addr, " Is a worker.")
                workers.append(client)
                workThread = threading.Thread(target=worker_handler, args=(
                    client, workers, requesters,), daemon=True)
                resultThread = threading.Thread(target=worker_result, args=(
                    client, requesters, workers, ), daemon=True)
                workerHandlers.append(client)
                workThread.start()
                resultThread.start()

        else:
            invalidMessage = ("Server did not recognize response, connection will close shortly.")
            client.send(invalidMessage.encode())
            time.sleep(5)
            client.close()

if __name__ == "__main__":
    main()
    

