import socket
import random 

host = "127.0.0.1"
port = 7777
banner = "== Guessing Game v1.0 =="

def generate_random_int(low, high):
    return random.randint(low, high)

# initialize the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print(f"server is listening on port {port}")
conn = None

while True:
    if conn is None:
        print("waiting for connection..")
        conn, addr = s.accept()
        print(f"new client: {addr[0]}")
    else:
        difficulty_choice = conn.recv(1024).decode().strip().lower()
        
        if difficulty_choice == 'a':
            low, high = 1, 50
        elif difficulty_choice == 'b':
            low, high = 1, 100
        elif difficulty_choice == 'c':
            low, high = 1, 500
        else:
            conn.sendall("Invalid choice. Please choose again.".encode())
            continue
        
        guessme = generate_random_int(low, high)
        difficulty_banner = f"{banner}\nDifficulty: {'Easy' if low == 1 and high == 50 else 'Medium' if low == 1 and high == 100 else 'Hard'}\n"
        conn.sendall(difficulty_banner.encode())

        while True:
            client_input = conn.recv(1024)
            guess = int(client_input.decode().strip())
            print(f"User guess attempt: {guess}")

            if guess == guessme:
                conn.sendall(b"Correct Answer!")
                play_again_data = conn.recv(1024).decode().strip().lower()
                if play_again_data == "yes":
                    break
                else:
                    conn.close()
                    conn = None
                    break
            elif guess > guessme:
                conn.sendall(b"Guess Lower!")
            elif guess < guessme:
                conn.sendall(b"Guess Higher!")
