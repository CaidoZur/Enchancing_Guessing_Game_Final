import socket
import random 

host = "127.0.0.1"
port = 7777
banner = "== Enchance Guessing Game =="
leaderboard_file = "leaderboard.txt"

def generate_random_int(low, high):
    return random.randint(low, high)

def load_leaderboard():
    leaderboard = {}
    try:
        with open(leaderboard_file, "r") as file:
            for line in file:
                username, score, last_difficulty = line.strip().split(",")
                leaderboard[username] = {"score": int(score), "last_difficulty": last_difficulty}
    except FileNotFoundError:
        pass
    return leaderboard

def save_leaderboard(leaderboard):
    with open(leaderboard_file, "w") as file:
        for username, info in leaderboard.items():
            file.write(f"{username}, (Attemps: {info['score']}), (Difficulty Level: {info['last_difficulty']})\n")

def format_leaderboard(leaderboard):
    formatted = "Leaderboard:\n"
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1]["score"])
    for idx, (username, info) in enumerate(sorted_leaderboard):
        formatted += f"{idx + 1}. {username} (Attempts: {info['score']}) (Difficulty Level: {info['last_difficulty'].upper()})\n"
    return formatted

# initialize the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print(f"server is listening on port {port}")
conn = None

leaderboard = load_leaderboard()

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
        
        username = conn.recv(1024).decode().strip()
        print(f"Username: {username}")

        user_info = leaderboard.get(username, {"score": float('inf'), "last_difficulty": "a"})
        user_score = user_info["score"]
        user_last_difficulty = user_info["last_difficulty"]

        if user_last_difficulty != difficulty_choice:
            user_score = float('inf')  # Reset the score if difficulty changed
        
        guessme = generate_random_int(low, high)
        difficulty_banner = f"{banner}\nDifficulty: {'Easy' if low == 1 and high == 50 else 'Medium' if low == 1 and high == 100 else 'Hard'}\n"
        conn.sendall(difficulty_banner.encode())

        attempt_count = 0
        while True:
            client_input = conn.recv(1024)
            guess = int(client_input.decode().strip())
            print(f"User guess attempt: {guess}")
            attempt_count += 1

            if guess == guessme:
                leaderboard[username] = {"score": min(user_score, attempt_count), "last_difficulty": difficulty_choice}
                save_leaderboard(leaderboard)
                conn.sendall(f"Correct Answer! Your guess tries: {attempt_count}\n{format_leaderboard(leaderboard)}".encode())
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