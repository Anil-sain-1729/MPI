from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = "tic-tac-toe-secret-key"

WINS = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
]

def new_game(mode="computer", score=None):
    return {
        "board": [""] * 9,
        "current": "X",
        "mode": mode,
        "winner": None,
        "game_over": False,
        "score": score or {"X": 0, "O": 0, "draw": 0}
    }

def get_game():
    if "game" not in session:
        session["game"] = new_game()
    return session["game"]

def save_game(game):
    session["game"] = game
    session.modified = True

def check_winner(board):
    for combo in WINS:
        a,b,c = combo
        if board[a] and board[a] == board[b] == board[c]:
            return board[a], combo
    if "" not in board:
        return "draw", []
    return None, []

def minimax(board, maximizing):
    winner, _ = check_winner(board)
    if winner == "O": return 1
    if winner == "X": return -1
    if winner == "draw": return 0

    if maximizing:
        best = -100
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                best = max(best, minimax(board, False))
                board[i] = ""
        return best
    else:
        best = 100
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                best = min(best, minimax(board, True))
                board[i] = ""
        return best

def computer_move(board):
    best = -100
    moves = []
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = ""
            if score > best:
                best = score
                moves = [i]
            elif score == best:
                moves.append(i)
    return random.choice(moves) if moves else None

@app.route("/")
def index():
    return render_template("index.html")

@app.get("/api/state")
def state():
    return jsonify({"success": True, "game": get_game()})

@app.post("/api/new-game")
def create_new_game():
    data = request.get_json(silent=True) or {}
    mode = data.get("mode", "computer")
    if mode not in ("computer", "player"):
        mode = "computer"

    old = get_game()
    game = new_game(mode, old.get("score"))
    save_game(game)
    return jsonify({"success": True, "game": game})

@app.post("/api/move")
def move():
    data = request.get_json(silent=True) or {}
    try:
        position = int(data.get("position"))
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Invalid position."}), 400

    if not 0 <= position <= 8:
        return jsonify({"success": False, "message": "Invalid position."}), 400

    game = get_game()

    if game["game_over"]:
        return jsonify({"success": False, "message": "Game is already over."})

    if game["mode"] == "computer" and game["current"] == "O":
        return jsonify({"success": False, "message": "Computer is thinking."})

    if game["board"][position]:
        return jsonify({"success": False, "message": "This box is already occupied."})

    player = game["current"]
    game["board"][position] = player

    winner, combo = check_winner(game["board"])

    if winner:
        game["game_over"] = True
        game["winner"] = winner
        game["score"]["draw" if winner == "draw" else winner] += 1
        save_game(game)
        return jsonify({
            "success": True,
            "game": game,
            "winner": winner,
            "combination": combo
        })

    if game["mode"] == "computer":
        game["current"] = "O"
        ai = computer_move(game["board"])

        if ai is not None:
            game["board"][ai] = "O"
            winner, combo = check_winner(game["board"])

            if winner:
                game["game_over"] = True
                game["winner"] = winner
                game["score"]["draw" if winner == "draw" else winner] += 1
                save_game(game)
                return jsonify({
                    "success": True,
                    "game": game,
                    "computer_move": ai,
                    "winner": winner,
                    "combination": combo
                })

        game["current"] = "X"
    else:
        game["current"] = "O" if player == "X" else "X"

    save_game(game)
    return jsonify({"success": True, "game": game})

@app.post("/api/reset-score")
def reset_score():
    game = get_game()
    game["score"] = {"X": 0, "O": 0, "draw": 0}
    save_game(game)
    return jsonify({"success": True, "game": game})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
