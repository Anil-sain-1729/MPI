import tkinter as tk
from tkinter import messagebox


# ============================================================
# DSA 15 PATTERNS VISUALIZER
# Python + Tkinter only
# ============================================================

BG = "#080b10"
CARD = "#11161d"
BORDER = "#26313d"
WHITE = "#eeeeee"
GRAY = "#8d99a6"
GREEN = "#00e5a0"
BLUE = "#22a7ff"
ORANGE = "#ffad42"
PURPLE = "#b985ff"
RED = "#ff5c67"
YELLOW = "#ffd447"


patterns = [
    ("1", "Two Pointers", BLUE),
    ("2", "Sliding Window", ORANGE),
    ("3", "Binary Search", GREEN),
    ("4", "Frequency Counting", PURPLE),
    ("5", "Matrix Traversal", YELLOW),
    ("6", "Monotonic Stack", RED),
    ("7", "Prefix Sum", GREEN),
    ("8", "Overlapping Intervals", PURPLE),
    ("9", "Greedy", YELLOW),
    ("10", "Top K Elements", ORANGE),
    ("11", "Backtracking", GREEN),
    ("12", "Binary Tree Traversal", PURPLE),
    ("13", "Depth-First Search", GREEN),
    ("14", "Breadth-First Search", BLUE),
    ("15", "Dynamic Programming", RED),
]


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()
root.title("DSA - 15 Patterns Visualizer")
root.geometry("1250x850")
root.configure(bg=BG)
root.minsize(950, 700)


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(root, bg=BG)
header.pack(fill="x", pady=(25, 10))

title = tk.Label(
    header,
    text="DSA was HARD until I learned these",
    font=("Arial", 27, "bold"),
    bg=BG,
    fg=WHITE
)
title.pack()

subtitle = tk.Label(
    header,
    text="15 PATTERNS",
    font=("Arial", 22, "bold"),
    bg="#00c98b",
    fg="#06100d",
    padx=30,
    pady=7
)
subtitle.pack(pady=10)


# ============================================================
# MAIN SCROLL AREA
# ============================================================

outer = tk.Frame(root, bg=BG)
outer.pack(fill="both", expand=True, padx=30, pady=10)

canvas = tk.Canvas(
    outer,
    bg=BG,
    highlightthickness=0
)

scrollbar = tk.Scrollbar(
    outer,
    orient="vertical",
    command=canvas.yview
)

canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

grid_frame = tk.Frame(canvas, bg=BG)

canvas_window = canvas.create_window(
    (0, 0),
    window=grid_frame,
    anchor="nw"
)


def update_scroll(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))


grid_frame.bind("<Configure>", update_scroll)


def resize_grid(event):
    canvas.itemconfig(canvas_window, width=event.width)


canvas.bind("<Configure>", resize_grid)


# ============================================================
# DRAWING HELPERS
# ============================================================

def box(c, x1, y1, x2, y2, text="",
        fill=CARD, outline=BORDER,
        color=WHITE, width=2, font=("Arial", 10, "bold")):

    c.create_rectangle(
        x1, y1, x2, y2,
        fill=fill,
        outline=outline,
        width=width
    )

    if text:
        c.create_text(
            (x1+x2)//2,
            (y1+y2)//2,
            text=text,
            fill=color,
            font=font
        )


def arrow(c, x1, y1, x2, y2, color=GREEN):
    c.create_line(
        x1, y1, x2, y2,
        fill=color,
        width=2,
        arrow=tk.LAST
    )


# ============================================================
# PREVIEW DRAWINGS
# ============================================================

def preview(c, number, color):

    c.delete("all")

    # --------------------------------------------------------
    # 1 TWO POINTERS
    # --------------------------------------------------------

    if number == "1":

        nums = [1, 3, 5, 7, 9, 11]

        for i, n in enumerate(nums):
            x = 15 + i * 38
            box(c, x, 45, x+30, 75, str(n),
                outline=color)

        c.create_text(
            27, 90, text="L",
            fill=GREEN,
            font=("Arial", 9, "bold")
        )

        c.create_text(
            217, 90, text="R",
            fill=RED,
            font=("Arial", 9, "bold")
        )

        arrow(c, 27, 40, 27, 25, GREEN)
        arrow(c, 217, 40, 217, 25, RED)

    # --------------------------------------------------------
    # 2 SLIDING WINDOW
    # --------------------------------------------------------

    elif number == "2":

        nums = [2, 1, 5, 1, 3, 2]

        for i, n in enumerate(nums):
            x = 12 + i * 39

            if 2 <= i <= 4:
                fill = "#5d4c15"
                outline = YELLOW
            else:
                fill = CARD
                outline = BORDER

            box(c, x, 48, x+31, 78,
                str(n), fill=fill,
                outline=outline)

        c.create_text(
            110, 25,
            text="WINDOW",
            fill=YELLOW,
            font=("Arial", 9, "bold")
        )

    # --------------------------------------------------------
    # 3 BINARY SEARCH
    # --------------------------------------------------------

    elif number == "3":

        nums = [1, 3, 5, 7, 9, 11, 13]

        for i, n in enumerate(nums):
            x = 10 + i * 40

            if n == 9:
                outline = GREEN
            else:
                outline = BORDER

            box(c, x, 48, x+32, 78,
                str(n), outline=outline)

        c.create_text(
            130, 25,
            text="L       M       R",
            fill=GREEN,
            font=("Arial", 9, "bold")
        )

    # --------------------------------------------------------
    # 4 FREQUENCY COUNTING
    # --------------------------------------------------------

    elif number == "4":

        letters = ["a", "b", "a", "c", "b"]

        for i, ch in enumerate(letters):
            x = 20 + i * 35
            box(c, x, 35, x+27, 62, ch,
                outline=PURPLE)

        box(c, 55, 72, 175, 105,
            "a = 2   b = 2   c = 1",
            outline=PURPLE,
            font=("Arial", 8, "bold"))

    # --------------------------------------------------------
    # 5 MATRIX TRAVERSAL
    # --------------------------------------------------------

    elif number == "5":

        num = 1

        for r in range(3):
            for col in range(4):

                x = 45 + col * 38
                y = 30 + r * 30

                box(
                    c,
                    x, y,
                    x+30, y+24,
                    str(num),
                    outline=YELLOW
                )

                num += 1

        arrow(c, 45, 20, 155, 20, GREEN)

    # --------------------------------------------------------
    # 6 MONOTONIC STACK
    # --------------------------------------------------------

    elif number == "6":

        nums = [1, 3, 2, 4]

        for i, n in enumerate(nums):
            x = 25 + i * 38
            box(c, x, 35, x+28, 62,
                str(n), outline=RED)

        box(c, 100, 75, 130, 105,
            "1",
            outline=BLUE)

        c.create_text(
            115, 115,
            text="STACK",
            fill=GRAY,
            font=("Arial", 8)
        )

    # --------------------------------------------------------
    # 7 PREFIX SUM
    # --------------------------------------------------------

    elif number == "7":

        nums = [1, 2, 3, 4]
        prefix = [0, 1, 3, 6, 10]

        for i, n in enumerate(prefix):
            x = 12 + i * 38

            box(
                c,
                x, 55,
                x+30, 82,
                str(n),
                outline=GREEN
            )

        c.create_text(
            100, 30,
            text="PREFIX",
            fill=GREEN,
            font=("Arial", 9, "bold")
        )

    # --------------------------------------------------------
    # 8 OVERLAPPING INTERVALS
    # --------------------------------------------------------

    elif number == "8":

        c.create_rectangle(
            30, 40, 120, 62,
            fill="#22536a",
            outline=BLUE
        )

        c.create_rectangle(
            85, 70, 190, 92,
            fill="#6b315c",
            outline=PURPLE
        )

        arrow(c, 120, 52, 150, 52, GREEN)

        c.create_text(
            105, 105,
            text="MERGE → [1, 6]",
            fill=GREEN,
            font=("Arial", 9, "bold")
        )

    # --------------------------------------------------------
    # 9 GREEDY
    # --------------------------------------------------------

    elif number == "9":

        nums = [25, 10, 5, 1]

        for i, n in enumerate(nums):

            x = 18 + i * 40

            outline = YELLOW if n == 5 else BORDER

            box(
                c,
                x, 50,
                x+32, 80,
                str(n),
                outline=outline
            )

        c.create_text(
            105, 25,
            text="AMOUNT = 5",
            fill=YELLOW,
            font=("Arial", 9, "bold")
        )

    # --------------------------------------------------------
    # 10 TOP K
    # --------------------------------------------------------

    elif number == "10":

        # small heap/tree

        c.create_oval(
            100, 20, 135, 55,
            fill="#44265c",
            outline=PURPLE,
            width=2
        )

        c.create_text(
            117, 37,
            text="3",
            fill=WHITE
        )

        c.create_line(
            117, 55, 85, 85,
            fill=PURPLE
        )

        c.create_line(
            117, 55, 150, 85,
            fill=PURPLE
        )

        c.create_oval(
            70, 75, 100, 105,
            outline=GREEN
        )

        c.create_text(
            85, 90,
            text="7",
            fill=WHITE
        )

        c.create_oval(
            135, 75, 165, 105,
            outline=GREEN
        )

        c.create_text(
            150, 90,
            text="5",
            fill=WHITE
        )

    # --------------------------------------------------------
    # 11 BACKTRACKING
    # --------------------------------------------------------

    elif number == "11":

        c.create_oval(
            105, 15, 135, 45,
            outline=GREEN,
            width=2
        )

        c.create_line(
            120, 45, 80, 75,
            fill=GRAY
        )

        c.create_line(
            120, 45, 160, 75,
            fill=GRAY
        )

        c.create_oval(
            65, 65, 95, 95,
            outline=GRAY
        )

        c.create_oval(
            145, 65, 175, 95,
            outline=GRAY
        )

        c.create_oval(
            65, 100, 95, 130,
            outline=RED
        )

        c.create_text(
            120, 125,
            text="EXPLORE → BACKTRACK",
            fill=GRAY,
            font=("Arial", 8)
        )

    # --------------------------------------------------------
    # 12 BINARY TREE
    # --------------------------------------------------------

    elif number == "12":

        c.create_oval(
            105, 15, 135, 45,
            outline=GREEN,
            width=2
        )

        c.create_line(
            120, 45, 80, 75,
            fill=GRAY
        )

        c.create_line(
            120, 45, 160, 75,
            fill=GRAY
        )

        for x, text, col in [
            (80, "2", GREEN),
            (160, "6", PURPLE)
        ]:

            c.create_oval(
                x-15, 65,
                x+15, 95,
                outline=col
            )

            c.create_text(
                x, 80,
                text=text,
                fill=WHITE
            )

    # --------------------------------------------------------
    # 13 DFS
    # --------------------------------------------------------

    elif number == "13":

        points = [
            (45, 45, "A"),
            (120, 25, "B"),
            (195, 45, "C"),
            (85, 90, "D"),
            (160, 90, "E")
        ]

        edges = [
            (0, 1),
            (1, 2),
            (0, 3),
            (3, 4),
            (2, 4)
        ]

        for a, b in edges:

            x1, y1, _ = points[a]
            x2, y2, _ = points[b]

            c.create_line(
                x1, y1,
                x2, y2,
                fill=BLUE,
                width=2
            )

        for x, y, text in points:

            c.create_oval(
                x-15, y-15,
                x+15, y+15,
                fill=CARD,
                outline=GREEN,
                width=2
            )

            c.create_text(
                x, y,
                text=text,
                fill=WHITE
            )

        c.create_text(
            120, 125,
            text="DFS: A → B → C",
            fill=GREEN,
            font=("Arial", 9, "bold")
        )

    # --------------------------------------------------------
    # 14 BFS
    # --------------------------------------------------------

    elif number == "14":

        points = [
            (45, 45, "A"),
            (120, 25, "B"),
            (195, 45, "C"),
            (85, 90, "D"),
            (160, 90, "E")
        ]

        edges = [
            (0, 1),
            (1, 2),
            (0, 3),
            (3, 4),
            (2, 4)
        ]

        for a, b in edges:

            x1, y1, _ = points[a]
            x2, y2, _ = points[b]

            c.create_line(
                x1, y1,
                x2, y2,
                fill=GRAY,
                width=2
            )

        for x, y, text in points:

            c.create_oval(
                x-15, y-15,
                x+15, y+15,
                fill=CARD,
                outline=BLUE,
                width=2
            )

            c.create_text(
                x, y,
                text=text,
                fill=WHITE
            )

        c.create_text(
            120, 125,
            text="BFS: A → B → D",
            fill=BLUE,
            font=("Arial", 9, "bold")
        )

    # --------------------------------------------------------
    # 15 DYNAMIC PROGRAMMING
    # --------------------------------------------------------

    elif number == "15":

        for r in range(2):

            for col in range(4):

                x = 40 + col * 38
                y = 35 + r * 35

                outline = RED

                if r == 0 and col == 2:
                    outline = BLUE

                box(
                    c,
                    x, y,
                    x+30, y+28,
                    str((r+1)*(col+1)),
                    outline=outline
                )

        c.create_text(
            115, 105,
            text="dp[i] = dp[i-1] + dp[i-2]",
            fill=RED,
            font=("Arial", 8, "bold")
        )


# ============================================================
# CARD CLICK
# ============================================================

def open_visualizer(number, name, color):

    win = tk.Toplevel(root)
    win.title(name + " - DSA Visualizer")
    win.geometry("900x650")
    win.configure(bg=BG)

    tk.Label(
        win,
        text=name,
        font=("Arial", 28, "bold"),
        bg=BG,
        fg=color
    ).pack(pady=(25, 5))

    tk.Label(
        win,
        text="Graphical Visualization",
        font=("Arial", 12),
        bg=BG,
        fg=GRAY
    ).pack()

    visual = tk.Canvas(
        win,
        bg="#0d1218",
        highlightthickness=1,
        highlightbackground=BORDER
    )

    visual.pack(
        fill="both",
        expand=True,
        padx=35,
        pady=25
    )

    # Draw large version
    draw_large_visual(visual, number, color)

    bottom = tk.Frame(win, bg=BG)
    bottom.pack(fill="x", pady=10)

    tk.Button(
        bottom,
        text="NEXT STEP",
        font=("Arial", 11, "bold"),
        bg=color,
        fg="#050505",
        relief="flat",
        padx=25,
        pady=10,
        command=lambda: animate_visual(
            visual, number, color
        )
    ).pack(side="left", padx=30)

    tk.Button(
        bottom,
        text="RESET",
        font=("Arial", 11, "bold"),
        bg=CARD,
        fg=WHITE,
        relief="flat",
        padx=25,
        pady=10,
        command=lambda: draw_large_visual(
            visual, number, color
        )
    ).pack(side="left")


# ============================================================
# LARGE VISUALIZER
# ============================================================

def draw_large_visual(c, number, color):

    c.delete("all")

    # TITLE
    c.create_text(
        450, 35,
        text="STEP-BY-STEP ALGORITHM",
        fill=GRAY,
        font=("Arial", 14, "bold")
    )

    # --------------------------------------------------------
    # TWO POINTERS
    # --------------------------------------------------------

    if number == "1":

        nums = [1, 3, 5, 7, 9, 11]

        for i, n in enumerate(nums):

            x = 130 + i * 100

            box(
                c,
                x, 230,
                x+70, 290,
                str(n),
                outline=color,
                width=3,
                font=("Arial", 16, "bold")
            )

        c.create_text(
            165, 190,
            text="L",
            fill=GREEN,
            font=("Arial", 16, "bold")
        )

        c.create_text(
            665, 190,
            text="R",
            fill=RED,
            font=("Arial", 16, "bold")
        )

        arrow(c, 165, 205, 165, 225, GREEN)
        arrow(c, 665, 205, 665, 225, RED)

        c.create_text(
            450, 360,
            text="Compare left and right → move pointers",
            fill=WHITE,
            font=("Arial", 17, "bold")
        )

    # --------------------------------------------------------
    # SLIDING WINDOW
    # --------------------------------------------------------

    elif number == "2":

        nums = [2, 1, 5, 1, 3, 2]

        for i, n in enumerate(nums):

            x = 100 + i * 105

            fill = "#594b12" if 1 <= i <= 3 else CARD

            box(
                c,
                x, 220,
                x+75, 280,
                str(n),
                fill=fill,
                outline=YELLOW if 1 <= i <= 3 else BORDER,
                width=3,
                font=("Arial", 16, "bold")
            )

        c.create_text(
            340, 175,
            text="WINDOW SIZE = 3",
            fill=YELLOW,
            font=("Arial", 18, "bold")
        )

        arrow(c, 200, 300, 410, 300, YELLOW)

    # --------------------------------------------------------
    # BINARY SEARCH
    # --------------------------------------------------------

    elif number == "3":

        nums = [1, 3, 5, 7, 9, 11, 13]

        for i, n in enumerate(nums):

            x = 80 + i * 105

            outline = GREEN if n == 7 else BORDER

            box(
                c,
                x, 230,
                x+75, 290,
                str(n),
                outline=outline,
                width=3,
                font=("Arial", 16, "bold")
            )

        c.create_text(
            395, 190,
            text="MID",
            fill=GREEN,
            font=("Arial", 16, "bold")
        )

        arrow(c, 415, 205, 415, 225, GREEN)

    # --------------------------------------------------------
    # MATRIX
    # --------------------------------------------------------

    elif number == "5":

        n = 1

        for r in range(4):

            for col in range(4):

                x = 270 + col * 90
                y = 130 + r * 90

                outline = GREEN

                box(
                    c,
                    x, y,
                    x+65, y+65,
                    str(n),
                    outline=outline,
                    width=3,
                    font=("Arial", 15, "bold")
                )

                n += 1

        c.create_text(
            450, 520,
            text="Traverse matrix in spiral order",
            fill=YELLOW,
            font=("Arial", 18, "bold")
        )

    # --------------------------------------------------------
    # TREE
    # --------------------------------------------------------

    elif number in ("11", "12"):

        # root
        c.create_line(
            450, 130,
            300, 250,
            fill=GRAY,
            width=4
        )

        c.create_line(
            450, 130,
            600, 250,
            fill=GRAY,
            width=4
        )

        c.create_line(
            300, 250,
            220, 380,
            fill=GRAY,
            width=4
        )

        c.create_line(
            300, 250,
            380, 380,
            fill=GRAY,
            width=4
        )

        c.create_line(
            600, 250,
            520, 380,
            fill=GRAY,
            width=4
        )

        c.create_line(
            600, 250,
            680, 380,
            fill=GRAY,
            width=4
        )

        nodes = [
            (450, 100, "4"),
            (300, 220, "2"),
            (600, 220, "6"),
            (220, 350, "1"),
            (380, 350, "3"),
            (520, 350, "5"),
            (680, 350, "7")
        ]

        for x, y, text in nodes:

            c.create_oval(
                x-35, y-35,
                x+35, y+35,
                fill=CARD,
                outline=color,
                width=4
            )

            c.create_text(
                x, y,
                text=text,
                fill=WHITE,
                font=("Arial", 18, "bold")
            )

        c.create_text(
            450, 470,
            text="1 → 2 → 3 → 4 → 5 → 6 → 7",
            fill=GREEN,
            font=("Arial", 18, "bold")
        )

    # --------------------------------------------------------
    # GRAPH DFS/BFS
    # --------------------------------------------------------

    elif number in ("13", "14"):

        points = {
            "A": (200, 200),
            "B": (450, 120),
            "C": (700, 200),
            "D": (300, 400),
            "E": (600, 400)
        }

        edges = [
            ("A", "B"),
            ("B", "C"),
            ("A", "D"),
            ("D", "E"),
            ("E", "C"),
            ("B", "E")
        ]

        for a, b in edges:

            x1, y1 = points[a]
            x2, y2 = points[b]

            c.create_line(
                x1, y1,
                x2, y2,
                fill=GRAY,
                width=4
            )

        for name, (x, y) in points.items():

            c.create_oval(
                x-40, y-40,
                x+40, y+40,
                fill=CARD,
                outline=color,
                width=4
            )

            c.create_text(
                x, y,
                text=name,
                fill=WHITE,
                font=("Arial", 18, "bold")
            )

        if number == "13":

            order = "DFS: A → B → C → E → D"

        else:

            order = "BFS: A → B → D → C → E"

        c.create_text(
            450, 540,
            text=order,
            fill=color,
            font=("Arial", 19, "bold")
        )

    # --------------------------------------------------------
    # DEFAULT ARRAY VISUALIZATION
    # --------------------------------------------------------

    else:

        nums = [1, 2, 3, 4, 5, 6]

        for i, n in enumerate(nums):

            x = 120 + i * 100

            box(
                c,
                x, 230,
                x+70, 290,
                str(n),
                outline=color,
                width=3,
                font=("Arial", 16, "bold")
            )

        c.create_text(
            450, 360,
            text="Algorithm visualization",
            fill=WHITE,
            font=("Arial", 20, "bold")
        )


# ============================================================
# SIMPLE ANIMATION / NEXT STEP
# ============================================================

def animate_visual(c, number, color):

    c.delete("animation")

    if number == "1":

        c.create_text(
            450, 430,
            text="L moves →",
            fill=GREEN,
            font=("Arial", 22, "bold"),
            tags="animation"
        )

    elif number == "2":

        c.create_text(
            450, 430,
            text="WINDOW SLIDES →",
            fill=YELLOW,
            font=("Arial", 22, "bold"),
            tags="animation"
        )

    elif number == "3":

        c.create_text(
            450, 430,
            text="MID = (L + R) // 2",
            fill=GREEN,
            font=("Arial", 22, "bold"),
            tags="animation"
        )

    elif number == "7":

        c.create_text(
            450, 430,
            text="prefix[i] = prefix[i-1] + nums[i]",
            fill=GREEN,
            font=("Arial", 20, "bold"),
            tags="animation"
        )

    elif number == "9":

        c.create_text(
            450, 430,
            text="Pick the largest value that fits",
            fill=YELLOW,
            font=("Arial", 20, "bold"),
            tags="animation"
        )

    elif number == "15":

        c.create_text(
            450, 430,
            text="dp[i] = dp[i-1] + dp[i-2]",
            fill=RED,
            font=("Arial", 20, "bold"),
            tags="animation"
        )

    else:

        c.create_text(
            450, 430,
            text="NEXT STEP →",
            fill=color,
            font=("Arial", 22, "bold"),
            tags="animation"
        )


# ============================================================
# CREATE CARDS
# ============================================================

def create_card(parent, number, name, color):

    card = tk.Frame(
        parent,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    # Header
    tk.Label(
        card,
        text=f"{number}. {name}",
        font=("Arial", 15, "bold"),
        bg=CARD,
        fg=color,
        anchor="w"
    ).pack(
        fill="x",
        padx=15,
        pady=(12, 5)
    )

    # Canvas preview
    c = tk.Canvas(
        card,
        width=235,
        height=145,
        bg=CARD,
        highlightthickness=0
    )

    c.pack(
        padx=8,
        pady=5
    )

    preview(c, number, color)

    # Click anywhere
    def click(event=None):
        open_visualizer(number, name, color)

    card.bind("<Button-1>", click)
    c.bind("<Button-1>", click)

    for widget in card.winfo_children():

        widget.bind(
            "<Button-1>",
            click
        )

    return card


# ============================================================
# GRID
# ============================================================

for i, (number, name, color) in enumerate(patterns):

    row = i // 3
    col = i % 3

    card = create_card(
        grid_frame,
        number,
        name,
        color
    )

    card.grid(
        row=row,
        column=col,
        padx=10,
        pady=10,
        sticky="nsew"
    )


for col in range(3):

    grid_frame.grid_columnconfigure(
        col,
        weight=1
    )


# ============================================================
# MOUSE WHEEL
# ============================================================

def mousewheel(event):

    canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


canvas.bind_all(
    "<MouseWheel>",
    mousewheel
)


# ============================================================
# FOOTER
# ============================================================

footer = tk.Label(
    root,
    text="Click any pattern to open its graphical visualization",
    bg=BG,
    fg=GRAY,
    font=("Arial", 10)
)

footer.pack(
    pady=(5, 15)
)


# ============================================================
# START
# ============================================================

root.mainloop()