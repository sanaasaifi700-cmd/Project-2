import tkinter as tk
import math

last_answer = "0"
scientific_widgets = []



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
            expression.set(str(math.factorial(int(num))))
            return

        expression.set(str(eval(expr)))

    except:
        expression.set("Error")


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



def build_buttons(scientific=False):
    """Builds the button layout depending on mode."""
    for widget in button_frame.winfo_children():
        widget.destroy()

    layout = scientific_buttons_full if scientific else basic_buttons

    scientific_symbols = ['sin', 'cos', 'tan', 'log', 'ln', 'π', '%',
                          '√', 'x²', 'x³', '!', 'e', '^']

    scientific_widgets.clear()

    for r, row in enumerate(layout):
        for c, char in enumerate(row):

            if char in ["C", "⌫", "="]:
                bg = "grey"
                fg = "white"
            else:
                bg = "white"
                fg = "black"

            if char == "C":
                cmd = clear_expression
            elif char == "⌫":
                cmd = backspace
            elif char == "=":
                cmd = calculate
            else:
                cmd = lambda ch=char: add_to_expression(ch)

            btn = tk.Button(button_frame, text=char, bg=bg, fg=fg,
                            font=("Arial", 16), command=cmd)

            if scientific and char == "=":
                btn.grid(row=r, column=c, columnspan=3, sticky="nsew", padx=3, pady=3)
                continue

            btn.grid(row=r, column=c, sticky="nsew", padx=3, pady=3)

            if char in scientific_symbols:
                scientific_widgets.append(btn)


    max_cols = max(len(row) for row in layout)
    for i in range(max_cols):
        button_frame.columnconfigure(i, weight=1)

    for i in range(len(layout)):
        button_frame.rowconfigure(i, weight=1)




root = tk.Tk()
root.title("Python Calculator")
root.geometry("400x530")
root.configure(bg="#D8BFD8")

expression = tk.StringVar()

entry = tk.Entry(root, textvariable=expression, font=("Arial", 22),
                 bd=5, relief=tk.RIDGE, justify="right")
entry.pack(fill="x", ipady=10, pady=10, padx=10)

is_scientific = tk.BooleanVar(value=False)

def toggle_mode():
    if is_scientific.get():
        is_scientific.set(False)
        toggle_btn.config(text="Switch to Scientific")
        build_buttons(scientific=False)
    else:
        is_scientific.set(True)
        toggle_btn.config(text="Switch to Basic")
        build_buttons(scientific=True)

toggle_btn = tk.Button(root, text="Switch to Scientific", font=("Arial", 14),
                       bg="black", fg="white", command=toggle_mode)
toggle_btn.pack(pady=5)

button_frame = tk.Frame(root, bg="#D8BFD8")
button_frame.pack(fill="both", expand=True)

build_buttons(scientific=False)

root.mainloop()
