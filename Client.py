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
        user_input = input("Enter your guess: ").strip()

        s.sendall(user_input.encode())
        reply = s.recv(1024).decode().strip()
        
        print(reply)

        if "Correct" in reply:
            break

def choose_difficulty():
    while True:
        print("Choose Difficulty Level:")
        print("a. Easy (1-50)")
        print("b. Medium (1-100)")
        print("c. Hard (1-500)")
        choice = input("Enter your choice (a/b/c): ").strip().lower()

        if choice in ['a', 'b', 'c']:
            s.sendall(choice.encode())
            break
        else:
            print("Invalid choice. Please choose again.")

choose_difficulty()
play_game()

while True:
    play_again = input("Do you want to play again? (yes/no): ").strip().lower()
    if play_again == "yes":
        s.sendall(play_again.encode())
        choose_difficulty()
        play_game()
    else:
        s.sendall("no".encode())
        break

s.close()
