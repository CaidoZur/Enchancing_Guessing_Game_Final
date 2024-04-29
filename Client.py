import socket

host = "127.0.0.1"
port = 7777

s = socket.socket()
s.connect((host, port))

def play_game():
    # received the banner
    data = s.recv(1024)
    # print banner
    print(data.decode().strip())

    while True:
        # let's get our input from the user
        user_input = input("").strip()

        s.sendall(user_input.encode())
        reply = s.recv(1024).decode().strip()
        
        print(reply)

        if "Correct" in reply:
            break

play_game()

while True:
    play_again = input("Do you want to play again? (yes/no): ").strip().lower()
    if play_again == "yes":
        s.sendall(play_again.encode())
        play_game()
    else:
        s.sendall("no".encode())
        break

s.close()
