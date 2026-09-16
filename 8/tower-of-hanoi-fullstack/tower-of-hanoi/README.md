# Tower of Hanoi - Full Stack Game

## Technologies
- Frontend: HTML, CSS, JavaScript
- Backend: Python, Flask
- API: REST-style JSON endpoints

## Features
- 3 to 8 discs
- Click-to-move
- Drag and drop
- Valid move checking
- Hint
- Undo
- Reset
- Auto Solve
- Pause / Resume
- Timer
- Move counter
- Minimum moves
- Progress
- Animated disc movement
- Moving arrow
- Win screen

## Run on Windows

```bash
cd tower-of-hanoi
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open:

http://127.0.0.1:5000

## Project Structure

tower-of-hanoi/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
