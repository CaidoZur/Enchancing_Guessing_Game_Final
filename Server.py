import socket
import random 

host = "127.0.0.1"
port = 7777
banner = """
== Guessing Game v1.0 ==
Enter your guess: """

def generate_random_int(low, high):
    return random.randint(low, high)

# initialize the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print(f"server is listening in port {port}")
guessme = 0
conn = None

while True:
    if conn is None:
        print("waiting for connection..")
        conn, addr = s.accept()
        guessme = generate_random_int(1, 100)
        print(f"new client: {addr[0]}")
        conn.sendall(banner.encode())
    else:
        play_again = True
        while play_again:
            client_input = conn.recv(1024)
            guess = int(client_input.decode().strip())
            print(f"User guess attempt: {guess}")
            if guess == guessme:
                conn.sendall(b"Correct Answer")
                play_again_data = conn.recv(1024).decode().strip().lower()
                if play_again_data == "yes":
                    guessme = generate_random_int(1, 100)
                    conn.sendall(banner.encode())
                else:
                    conn.close()
                    conn = None
                    play_again = False
            elif guess > guessme:
                conn.sendall(b"Guess Lower!")
            elif guess < guessme:
                conn.sendall(b"Guess Higher!")
