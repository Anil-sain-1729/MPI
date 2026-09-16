from flask import Flask, render_template, request, jsonify, session
from collections import deque
import copy

app = Flask(__name__)
app.secret_key = "tower-of-hanoi-secret-key"

MIN_DISCS = 3
MAX_DISCS = 8

def create_game(discs=3):
    return {
        "n": discs,
        "towers": [list(range(discs, 0, -1)), [], []],
        "moves": 0,
        "history": []
    }

def get_game():
    if "game" not in session:
        session["game"] = create_game(3)
    return session["game"]

def save_game(game):
    session["game"] = game
    session.modified = True

def minimum_moves(n):
    return (2 ** n) - 1

def is_won(game):
    return len(game["towers"][2]) == game["n"]

def public_state(game):
    return {
        "n": game["n"],
        "towers": game["towers"],
        "moves": game["moves"],
        "minimum": minimum_moves(game["n"]),
        "won": is_won(game)
    }

def legal_moves(towers):
    moves = []
    for source in range(3):
        if not towers[source]:
            continue
        disc = towers[source][-1]
        for destination in range(3):
            if source == destination:
                continue
            if not towers[destination] or towers[destination][-1] > disc:
                moves.append((source, destination, disc))
    return moves

def towers_to_position(towers, n):
    position = [0] * n
    for tower_index, tower in enumerate(towers):
        for disc in tower:
            position[disc - 1] = tower_index
    return tuple(position)

def position_to_towers(position, n):
    towers = [[], [], []]
    for disc in range(n, 0, -1):
        towers[position[disc - 1]].append(disc)
    return towers

def shortest_solution(towers, n):
    start = towers_to_position(towers, n)
    goal = tuple([2] * n)
    if start == goal:
        return []

    queue = deque([start])
    parent = {start: None}
    move_used = {}

    while queue:
        current = queue.popleft()
        current_towers = position_to_towers(current, n)

        for source, destination, disc in legal_moves(current_towers):
            next_position = list(current)
            next_position[disc - 1] = destination
            next_position = tuple(next_position)

            if next_position in parent:
                continue

            parent[next_position] = current
            move_used[next_position] = (source, destination, disc)

            if next_position == goal:
                path = []
                state = next_position
                while parent[state] is not None:
                    path.append(move_used[state])
                    state = parent[state]
                path.reverse()
                return path

            queue.append(next_position)

    return []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/state")
def state():
    game = get_game()
    return jsonify({"success": True, "state": public_state(game)})

@app.post("/api/new-game")
def new_game():
    data = request.get_json(silent=True) or {}
    try:
        discs = int(data.get("discs", 3))
    except (TypeError, ValueError):
        discs = 3

    discs = max(MIN_DISCS, min(MAX_DISCS, discs))
    game = create_game(discs)
    save_game(game)
    return jsonify({"success": True, "message": "New game created.", "state": public_state(game)})

@app.post("/api/reset")
def reset():
    game = get_game()
    game = create_game(game["n"])
    save_game(game)
    return jsonify({"success": True, "message": "Game reset.", "state": public_state(game)})

@app.post("/api/move")
def make_move():
    data = request.get_json(silent=True) or {}

    try:
        source = int(data["source"])
        destination = int(data["destination"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"success": False, "message": "Invalid move data."}), 400

    if source not in range(3) or destination not in range(3):
        return jsonify({"success": False, "message": "Invalid tower."}), 400

    if source == destination:
        return jsonify({"success": False, "message": "Source and destination cannot be same."}), 400

    game = get_game()
    towers = game["towers"]

    if not towers[source]:
        return jsonify({"success": False, "message": "Source tower is empty."}), 400

    moving_disc = towers[source][-1]

    if towers[destination] and moving_disc > towers[destination][-1]:
        return jsonify({
            "success": False,
            "message": "You cannot place a larger disc on a smaller disc."
        }), 400

    game["history"].append({
        "towers": copy.deepcopy(towers),
        "moves": game["moves"]
    })

    towers[source].pop()
    towers[destination].append(moving_disc)
    game["moves"] += 1
    save_game(game)

    return jsonify({
        "success": True,
        "message": f"Move disc {moving_disc} from tower {source + 1} to tower {destination + 1}.",
        "disc": moving_disc,
        "source": source,
        "destination": destination,
        "state": public_state(game)
    })

@app.post("/api/undo")
def undo():
    game = get_game()

    if not game["history"]:
        return jsonify({
            "success": False,
            "message": "Nothing to undo.",
            "state": public_state(game)
        })

    previous = game["history"].pop()
    game["towers"] = previous["towers"]
    game["moves"] = previous["moves"]
    save_game(game)

    return jsonify({
        "success": True,
        "message": "Previous move restored.",
        "state": public_state(game)
    })

@app.post("/api/hint")
def hint():
    game = get_game()
    solution = shortest_solution(game["towers"], game["n"])

    if not solution:
        return jsonify({
            "success": True,
            "message": "Puzzle already solved." if is_won(game) else "No solution found.",
            "hint": None
        })

    source, destination, disc = solution[0]

    reason = (
        f"Move disc {disc} to tower {destination + 1}."
        if not game["towers"][destination]
        else f"Move disc {disc} on top of disc {game['towers'][destination][-1]}."
    )

    return jsonify({
        "success": True,
        "hint": {
            "source": source,
            "destination": destination,
            "disc": disc,
            "reason": reason
        },
        "message": f"Hint: move disc {disc} from tower {source + 1} to tower {destination + 1}."
    })

@app.post("/api/auto-solve")
def auto_solve():
    game = get_game()
    solution = shortest_solution(game["towers"], game["n"])

    moves = [
        {"source": source, "destination": destination, "disc": disc}
        for source, destination, disc in solution
    ]

    return jsonify({"success": True, "moves": moves, "count": len(moves)})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
