import socket
import itertools
import string
import hashlib
import time

HOST = '127.0.0.1'
PORT = 1234


def guess_generator(s, numbers, hashed):
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    iterator = 0
    done = 0

 
    while iterator <= len(numbers):

        for guess in itertools.product(chars, repeat=numbers[iterator]):
            iteration = (''.join(guess))
            iterationHash = hashlib.md5(iteration.encode()).hexdigest()

            if iterationHash == hashed:
                done = 1
                success = 'The password is: ' + iteration
                s.send(success.encode())
                print(success)
                print(
                    "Thank you for contributing to the crack! The program will close in ten seconds.")
                time.sleep(10)
                exit()
                break

        if done == 1:
            break
        iterator += 1
    time.sleep(10)

def communicate_to_server(s):
     # Main method used for majority of printing out to terminal
    print("Thank you for contributing to the password crack!")
    print("We will be borrowing some processing power before automatically closing this window.")
    parameters = s.recv(1024).decode()
    if parameters == 'Number of workers at capacity, connection dropped.':
        print(parameters)
    while True:
        hashed = s.recv(1024).decode()
        if hashed != "" and len(hashed) > 6:
            print('Parameters are: ' + parameters)
            print('Correct hash is: ' + hashed)
            print("Working. . .")
            numbers = list()

            # Loop to convert string parameters to integers
            for character in parameters:
                numbers.append(int(character))
            guess_generator(s, numbers, hashed)

def main():
# Sets up sockets / variables needed for connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    identifier = "2"

    s.connect((HOST, PORT))
    s.send(identifier.encode())
    communicate_to_server(s)

   

if __name__ == "__main__":
    main()