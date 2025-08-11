import os
import platform
import json
from datetime import datetime

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def print_board(board):
    print()
    for row in range(3):
        print(" ", end="")
        for col in range(3):
            mark = board[row][col]
            if mark == 0:
                print(f" {3*row + col + 1} ", end="")
            elif mark == 1:
                print(" X ", end="")
            else:
                print(" O ", end="")
            if col < 2:
                print("|", end="")
        print()
        if row < 2:
            print(" ---+---+---")
    print()

def check_win(board, player):
    for row in range(3):
        if all([board[row][col] == player for col in range(3)]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]):
        return True
    if all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False

def board_full(board):
    for row in board:
        for cell in row:
            if cell == 0:
                return False
    return True

def print_winner_box(text):
    length = len(text) + 4
    print("\n" + "*" * length)
    print(f"* {text} *")
    print("*" * length + "\n")

def wait_for_enter():
    input("Press Enter to continue...")

def save_stats(player1, player2, data):
    # ساخت نام فایل بر اساس نام پلیرها، فقط حروف و اعداد لاتین نگه داشته میشن
    def clean_name(name):
        return "".join(c for c in name if c.isalnum())

    filename = f"{clean_name(player1)}_{clean_name(player2)}_stats.json"
    try:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                stats = json.load(f)
        else:
            stats = []

        stats.append(data)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=4)

        print(f"\nStats saved to {filename} successfully!")
    except Exception as e:
        print(f"\nError saving stats: {e}")

def game_loop():
    clear_screen()
    print("=== ASD (Amjadi-style Doze) ===\n")

    player1_name = input("Name Player 1 (X): ").strip()
    while not player1_name:
        player1_name = input("Name nemitavanad khali bashad. Lotfan Name Player 1 ra vared konid: ").strip()

    player2_name = input("Name Player 2 (O): ").strip()
    while not player2_name:
        player2_name = input("Name nemitavanad khali bashad. Lotfan Name Player 2 ra vared konid: ").strip()

    while True:
        rounds_input = input("Tedade round (between 3 and 5): ").strip()
        if rounds_input.isdigit():
            rounds = int(rounds_input)
            if 3 <= rounds <= 5:
                break
        print("Lotfan adadi beyn 3 ta 5 vared konid.")

    score = {player1_name:0, player2_name:0}

    for round_number in range(1, rounds + 1):
        board = [[0]*3 for _ in range(3)]
        player = 1

        while True:
            clear_screen()
            print(f"Round {round_number} az {rounds}\n")
            print(f"Scoreha: {player1_name} = {score[player1_name]}   |   {player2_name} = {score[player2_name]}\n")
            print_board(board)

            current_player_name = player1_name if player == 1 else player2_name
            print(f"Nobate shoma ast, {current_player_name} ({'X' if player == 1 else 'O'})\n")

            move = input("Number Khane (1-9) ra vared konid: ").strip()

            if not move.isdigit():
                print("\nError: Adadi motabar vared konid!")
                wait_for_enter()
                continue
            pos = int(move)
            if pos < 1 or pos > 9:
                print("\nError: Adad bayad beyn 1 ta 9 bashad!")
                wait_for_enter()
                continue

            row = (pos - 1) // 3
            col = (pos - 1) % 3

            if board[row][col] != 0:
                print("\nError: In khane ghablan por shode, lotfan dobare talash konid!")
                wait_for_enter()
                continue

            board[row][col] = player

            if check_win(board, player):
                clear_screen()
                print(f"Round {round_number} az {rounds}\n")
                print(f"Scoreha: {player1_name} = {score[player1_name]}   |   {player2_name} = {score[player2_name]}\n")
                print_board(board)
                print_winner_box(f"Tabrik! {current_player_name} barande in round shod!")
                score[current_player_name] += 1
                wait_for_enter()
                break

            if board_full(board):
                clear_screen()
                print(f"Round {round_number} az {rounds}\n")
                print(f"Scoreha: {player1_name} = {score[player1_name]}   |   {player2_name} = {score[player2_name]}\n")
                print_board(board)
                print_winner_box("In round mosavi shod!")
                wait_for_enter()
                break

            player = 2 if player == 1 else 1

    clear_screen()
    print("=== Bazi tamam shod ===\n")
    print(f"Final Score:\n{player1_name} = {score[player1_name]}\n{player2_name} = {score[player2_name]}\n")

    if score[player1_name] > score[player2_name]:
        winner_text = f"🏆 Barande kol: {player1_name} 🏆"
    elif score[player1_name] < score[player2_name]:
        winner_text = f"🏆 Barande kol: {player2_name} 🏆"
    else:
        winner_text = "Bazi mosavi shod!"

    print_winner_box(winner_text)

    while True:
        print("1 - Bazi ro dobare shoro kon")
        print("2 - Save stats va khoroji")
        choice = input("Entekhab shoma: ").strip()
        if choice == "1":
            return False  # restart game
        elif choice == "2":
            data = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "player1": player1_name,
                "player2": player2_name,
                "rounds": rounds,
                "score": score,
                "winner": winner_text,
            }
            save_stats(player1_name, player2_name, data)
            print("Bye!")
            return True  # exit game
        else:
            print("Lotfan 1 ya 2 ra vared konid.")

def main():
    while True:
        exit_game = game_loop()
        if exit_game:
            break

if __name__ == "__main__":
    main()
