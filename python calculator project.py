import tkinter as tk
import math

last_answer = "0"
scientific_widgets = []
history_list = []

def add_to_expression(value):
    expression.set(expression.get() + str(value))

def clear_expression():
    expression.set("")

def backspace():
    current = expression.get()
    expression.set(current[:-1])

def calculate():
    global last_answer
    try:
        expr = expression.get()
        expr = expr.replace("sin", "math.sin")
        expr = expr.replace("cos", "math.cos")
        expr = expr.replace("tan", "math.tan")
        expr = expr.replace("log", "math.log10")
        expr = expr.replace("ln", "math.log")
        expr = expr.replace("^", "**")
        expr = expr.replace("π", "math.pi")
        expr = expr.replace("e", "math.e")
        expr = expr.replace("%", "*0.01")
        expr = expr.replace("√", "math.sqrt")
        expr = expr.replace("x²", "**2")
        expr = expr.replace("x³", "**3")

        if "!" in expression.get():
            num = expression.get().replace("!", "")
            result = str(math.factorial(int(num)))
            expression.set(result)
        else:
            result = str(eval(expr))

        expression.set(result)
        last_answer = result
        add_to_history(expr, result)

    except:
        expression.set("Error")

def add_to_history(expr, result):
    item = f"{expr} = {result}"
    history_list.append(item)
    history_box.insert(tk.END, item)
    history_box.yview(tk.END)

def use_history(event):
    selected = history_box.get(history_box.curselection())
    if selected:
        expr = selected.split('=')[0].strip()
        expression.set(expr)

def toggle_history():
    if history_frame.winfo_ismapped():
        history_frame.pack_forget()
    else:
        history_frame.pack(fill="x", padx=10, pady=(5,5))

def clear_history():
    history_list.clear()
    history_box.delete(0, tk.END)

def key_input(event):
    if event.char in "0123456789+-*/().":
        add_to_expression(event.char)
    elif event.keysym == "Return":
        calculate()
    elif event.keysym == "BackSpace":
        backspace()

root = tk.Tk()
root.title("Python Calculator")
root.geometry("395x540")
root.configure(bg="#D8BFD8")

expression = tk.StringVar()
entry = tk.Entry(root, textvariable=expression, font=("Arial", 22),
                 bd=5, relief=tk.RIDGE, justify="right")
entry.pack(fill="x", ipady=10, pady=10, padx=10)

button_top_frame = tk.Frame(root, bg="#D8BFD8")
button_top_frame.pack(fill="x", padx=10, pady=5)

is_scientific = tk.BooleanVar(value=False)

def toggle_mode():
    if is_scientific.get():
        is_scientific.set(False)
        mode_btn.config(text="Scientific")
        build_buttons(False)
    else:
        is_scientific.set(True)
        mode_btn.config(text="Basic")
        build_buttons(True)

mode_btn = tk.Button(button_top_frame, text="Scientific", font=("Arial", 12),
                     bg="black", fg="white", command=toggle_mode)
mode_btn.grid(row=0, column=0, sticky="nsew", padx=3)

history_btn = tk.Button(button_top_frame, text="History", font=("Arial", 12),
                        bg="purple", fg="white", command=toggle_history)
history_btn.grid(row=0, column=1, sticky="nsew", padx=3)

button_top_frame.columnconfigure(0, weight=1)
button_top_frame.columnconfigure(1, weight=1)

history_frame = tk.Frame(root)
history_box = tk.Listbox(history_frame, height=5, font=("Arial", 12))
history_box.pack(fill="x")
history_box.bind("<Double-Button-1>", use_history)

scrollbar = tk.Scrollbar(history_box, orient="vertical")
scrollbar.pack(side="right", fill="y")
history_box.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=history_box.yview)

clear_hist_btn = tk.Button(history_frame, text="Clear History", font=("Arial", 10),
                           bg="red", fg="white", command=clear_history)
clear_hist_btn.pack(pady=2)

basic_buttons = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', '(', ')', '+'],
    ['.', 'C', '⌫', '=']
]

scientific_buttons_full = [
    ['7', '8', '9', '/', 'sin'],
    ['4', '5', '6', '*', 'cos'],
    ['1', '2', '3', '-', 'tan'],
    ['0', '.', '^', '+', 'log'],
    ['(', ')', 'ln', 'π', '%'],
    ['√', 'x²', 'x³', '!', 'e'],
    ['C', '⌫', '=']
]

button_frame = tk.Frame(root, bg="#D8BFD8")
button_frame.pack(fill="both", expand=True, padx=10, pady=10)

def build_buttons(scientific=False):
    for widget in button_frame.winfo_children():
        widget.destroy()

    layout = scientific_buttons_full if scientific else basic_buttons

    for r, row in enumerate(layout):
        for c, char in enumerate(row):
            if char in ["C", "⌫", "="]:
                bg = "grey"; fg = "white"
            else:
                bg = "white"; fg = "black"

            if char == "C": cmd = clear_expression
            elif char == "⌫": cmd = backspace
            elif char == "=": cmd = calculate
            else: cmd = lambda ch=char: add_to_expression(ch)

            btn = tk.Button(button_frame, text=char, bg=bg, fg=fg,
                            font=("Arial", 16), command=cmd)

            if scientific and char == "=":
                btn.grid(row=r, column=c, columnspan=3, sticky="nsew", padx=3, pady=3)
                continue

            btn.grid(row=r, column=c, sticky="nsew", padx=3, pady=3)

    max_cols = max(len(row) for row in layout)
    for i in range(max_cols):
        button_frame.columnconfigure(i, weight=1)
    for i in range(len(layout)):
        button_frame.rowconfigure(i, weight=1)

build_buttons(False)

root.bind("<Key>", key_input)

root.mainloop()
 