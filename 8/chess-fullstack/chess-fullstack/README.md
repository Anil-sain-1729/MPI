# Chess Arena — Full Stack

A beginner-friendly browser chess game using:

- HTML
- CSS
- JavaScript
- Python + Flask

## Features

- 8×8 chess board
- White and Black pieces
- Click-to-move interface
- Legal move validation on the Python backend
- Check, checkmate and stalemate detection
- Move highlighting
- Last-move highlighting
- Undo
- New Game
- Automatic pawn promotion to Queen
- Responsive dark UI

## Run

1. Open terminal in this folder.
2. Create a virtual environment (optional):

   Windows:
   `python -m venv venv`
   `venv\Scripts\activate`

3. Install:
   `pip install -r requirements.txt`

4. Start:
   `python app.py`

5. Open:
   `http://127.0.0.1:5000`

## Note

This version intentionally keeps the core implementation dependency-light. Castling and en-passant are not included yet; pawn promotion is automatic to Queen.
