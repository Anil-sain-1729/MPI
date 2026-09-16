from flask import Flask, render_template, request, jsonify, session
import copy

app = Flask(__name__)
app.secret_key = "chess-demo-secret-key"

# Board: uppercase = White, lowercase = Black
# r n b q k b n r
# p p p p p p p p
# . . . . . . . .
# . . . . . . . .
# . . . . . . . .
# . . . . . . . .
# P P P P P P P P
# R N B Q K B N R

START = [
    list("rnbqkbnr"),
    list("pppppppp"),
    list("........"),
    list("........"),
    list("........"),
    list("........"),
    list("PPPPPPPP"),
    list("RNBQKBNR"),
]

PIECE_VALUES = {"p":100, "n":320, "b":330, "r":500, "q":900, "k":20000}

def fresh_game():
    return {
        "board": copy.deepcopy(START),
        "turn": "w",
        "history": [],
        "status": "playing",
        "winner": None,
        "last_move": None
    }

def color(piece):
    if piece == ".":
        return None
    return "w" if piece.isupper() else "b"

def inside(r,c):
    return 0 <= r < 8 and 0 <= c < 8

def pseudo_moves(board, r, c):
    piece = board[r][c]
    if piece == ".": return []
    p = piece.lower()
    own = color(piece)
    out = []

    def add(nr,nc):
        if inside(nr,nc):
            target = board[nr][nc]
            if target == "." or color(target) != own:
                out.append((nr,nc))

    if p == "p":
        d = -1 if own == "w" else 1
        start = 6 if own == "w" else 1
        nr = r+d
        if inside(nr,c) and board[nr][c] == ".":
            out.append((nr,c))
            nr2 = r+2*d
            if r == start and board[nr2][c] == ".":
                out.append((nr2,c))
        for dc in (-1,1):
            nr,nc = r+d,c+dc
            if inside(nr,nc) and board[nr][nc] != "." and color(board[nr][nc]) != own:
                out.append((nr,nc))
    elif p == "n":
        for dr,dc in ((2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)):
            add(r+dr,c+dc)
    elif p == "k":
        for dr in (-1,0,1):
            for dc in (-1,0,1):
                if dr or dc: add(r+dr,c+dc)
    else:
        dirs = []
        if p in ("b","q"): dirs += [(1,1),(1,-1),(-1,1),(-1,-1)]
        if p in ("r","q"): dirs += [(1,0),(-1,0),(0,1),(0,-1)]
        for dr,dc in dirs:
            nr,nc = r+dr,c+dc
            while inside(nr,nc):
                if board[nr][nc] == ".":
                    out.append((nr,nc))
                else:
                    if color(board[nr][nc]) != own: out.append((nr,nc))
                    break
                nr,nc = nr+dr,nc+dc
    return out

def find_king(board, side):
    k = "K" if side == "w" else "k"
    for r in range(8):
        for c in range(8):
            if board[r][c] == k:
                return (r,c)
    return None

def square_attacked(board, r, c, by_side):
    # Pawn attacks
    pr = r+1 if by_side == "w" else r-1
    for pc in (c-1,c+1):
        if inside(pr,pc) and board[pr][pc] == ("P" if by_side=="w" else "p"):
            return True
    # Knights
    knight = "N" if by_side=="w" else "n"
    for dr,dc in ((2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)):
        rr,cc=r+dr,c+dc
        if inside(rr,cc) and board[rr][cc]==knight: return True
    # King
    king = "K" if by_side=="w" else "k"
    for dr in (-1,0,1):
        for dc in (-1,0,1):
            if (dr or dc) and inside(r+dr,c+dc) and board[r+dr][c+dc]==king:
                return True
    # Sliding pieces
    enemy_b = "B" if by_side=="w" else "b"
    enemy_r = "R" if by_side=="w" else "r"
    enemy_q = "Q" if by_side=="w" else "q"
    for dr,dc in ((1,1),(1,-1),(-1,1),(-1,-1)):
        rr,cc=r+dr,c+dc
        while inside(rr,cc):
            if board[rr][cc] != ".":
                if board[rr][cc] in (enemy_b,enemy_q): return True
                break
            rr,cc=rr+dr,cc+dc
    for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
        rr,cc=r+dr,c+dc
        while inside(rr,cc):
            if board[rr][cc] != ".":
                if board[rr][cc] in (enemy_r,enemy_q): return True
                break
            rr,cc=rr+dr,cc+dc
    return False

def in_check(board, side):
    k = find_king(board, side)
    return k is None or square_attacked(board, k[0], k[1], "b" if side=="w" else "w")

def apply_move(board, fr,fc,tr,tc):
    b=copy.deepcopy(board)
    piece=b[fr][fc]
    b[tr][tc]=piece
    b[fr][fc]="."
    # Auto promote to queen
    if piece=="P" and tr==0: b[tr][tc]="Q"
    if piece=="p" and tr==7: b[tr][tc]="q"
    return b

def legal_moves(board, side):
    moves=[]
    for r in range(8):
        for c in range(8):
            if color(board[r][c]) != side: continue
            for tr,tc in pseudo_moves(board,r,c):
                # Don't allow capturing the enemy king directly
                if board[tr][tc].lower()=="k": continue
                nb=apply_move(board,r,c,tr,tc)
                if not in_check(nb,side):
                    moves.append((r,c,tr,tc))
    return moves

def notation(fr,fc,tr,tc,piece):
    files="abcdefgh"
    return f"{piece.upper()}{files[fc]}{8-fr}-{files[tc]}{8-tr}"

def game_state(g):
    side=g["turn"]
    moves=legal_moves(g["board"],side)
    if not moves:
        if in_check(g["board"],side):
            g["status"]="checkmate"; g["winner"]="b" if side=="w" else "w"
        else:
            g["status"]="draw"; g["winner"]=None
    elif in_check(g["board"],side):
        g["status"]="check"
    else:
        g["status"]="playing"
    return g

@app.route("/")
def index():
    return render_template("index.html")

@app.get("/api/state")
def state():
    g=session.get("game") or fresh_game()
    g=game_state(g)
    session["game"]=g
    return jsonify(g)

@app.post("/api/new-game")
def new_game():
    session["game"]=fresh_game()
    return jsonify(session["game"])

@app.post("/api/move")
def move():
    g=session.get("game") or fresh_game()
    data=request.get_json(silent=True) or {}
    try:
        fr,fc,tr,tc=[int(data[k]) for k in ("fr","fc","tr","tc")]
    except Exception:
        return jsonify({"error":"Invalid move data"}),400
    side=g["turn"]
    if g["status"] in ("checkmate","draw"):
        return jsonify({"error":"Game is over"}),400
    legal=legal_moves(g["board"],side)
    if (fr,fc,tr,tc) not in legal:
        return jsonify({"error":"Illegal move"}),400
    piece=g["board"][fr][fc]
    captured=g["board"][tr][tc]
    g["history"].append({
        "board":copy.deepcopy(g["board"]),
        "turn":g["turn"],
        "last_move":g.get("last_move")
    })
    g["board"]=apply_move(g["board"],fr,fc,tr,tc)
    g["last_move"]=[fr,fc,tr,tc]
    g["turn"]="b" if side=="w" else "w"
    game_state(g)
    session["game"]=g
    return jsonify(g)

@app.post("/api/undo")
def undo():
    g=session.get("game") or fresh_game()
    if g["history"]:
        old=g["history"].pop()
        g["board"]=old["board"]
        g["turn"]=old["turn"]
        g["last_move"]=old["last_move"]
        g["status"]="playing"; g["winner"]=None
        game_state(g)
    session["game"]=g
    return jsonify(g)

if __name__ == "__main__":
    app.run(debug=True)
