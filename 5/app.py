import tkinter as tk

app = tk.Tk()
app.title("BookConnect")
app.geometry("1000x650")
app.configure(bg="#f7f2ea")

title = tk.Label(
    app,
    text="📚 BookConnect",
    font=("Arial", 32, "bold"),
    bg="#f7f2ea",
    fg="#5b1730"
)
title.pack(pady=40)

subtitle = tk.Label(
    app,
    text="Books Connect People.",
    font=("Arial", 24),
    bg="#f7f2ea",
    fg="#30221d"
)
subtitle.pack(pady=10)

description = tk.Label(
    app,
    text="A platform connecting Writers, Printers, Delivery Boys and Readers.",
    font=("Arial", 14),
    bg="#f7f2ea"
)
description.pack(pady=10)


def writer():
    print("Writer Selected")


def printer():
    print("Printer Selected")


def reader():
    print("Reader Selected")


def delivery():
    print("Delivery Boy Selected")


frame = tk.Frame(app, bg="#f7f2ea")
frame.pack(pady=50)

tk.Button(
    frame,
    text="✍️ Writer",
    command=writer,
    width=18,
    height=3,
    font=("Arial", 14, "bold")
).grid(row=0, column=0, padx=15)

tk.Button(
    frame,
    text="🖨️ Printer",
    command=printer,
    width=18,
    height=3,
    font=("Arial", 14, "bold")
).grid(row=0, column=1, padx=15)

tk.Button(
    frame,
    text="📖 Reader",
    command=reader,
    width=18,
    height=3,
    font=("Arial", 14, "bold")
).grid(row=0, column=2, padx=15)

tk.Button(
    frame,
    text="🚚 Delivery Boy",
    command=delivery,
    width=18,
    height=3,
    font=("Arial", 14, "bold")
).grid(row=0, column=3, padx=15)


footer = tk.Label(
    app,
    text="BookConnect © 2026",
    font=("Arial", 11),
    bg="#f7f2ea",
    fg="#666"
)
footer.pack(side="bottom", pady=25)

app.mainloop()