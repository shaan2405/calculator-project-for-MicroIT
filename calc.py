import tkinter as tk
from tkinter import font as tkfont
from math import sqrt, factorial, log10, log, sin, cos, tan, radians


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Modern Calculator")
        self.geometry("400x600")
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")

        # Custom font
        self.custom_font = tkfont.Font(family="Helvetica", size=20)
        self.small_font = tkfont.Font(family="Helvetica", size=14)

        # Variables
        self.current_input = ""
        self.total_expression = ""
        self.display_var = tk.StringVar()
        self.history_var = tk.StringVar()

        self.create_display()
        self.create_buttons()

        # Key bindings
        self.bind("<Key>", self.key_press)

    def create_display(self):
        # History display (smaller text)
        history_frame = tk.Frame(self, height=50, bg="#f0f0f0")
        history_frame.pack(expand=True, fill="both", padx=10, pady=(10, 0))

        history_label = tk.Label(
            history_frame,
            textvariable=self.history_var,
            anchor="e",
            bg="#f0f0f0",
            fg="#666",
            font=self.small_font
        )
        history_label.pack(expand=True, fill="both")

        # Main display
        display_frame = tk.Frame(self, height=80, bg="#f0f0f0")
        display_frame.pack(expand=True, fill="both", padx=10, pady=(0, 10))

        display_label = tk.Label(
            display_frame,
            textvariable=self.display_var,
            anchor="e",
            bg="#f0f0f0",
            fg="#000",
            font=self.custom_font
        )
        display_label.pack(expand=True, fill="both")

    def create_buttons(self):
        buttons_frame = tk.Frame(self, bg="#f0f0f0")
        buttons_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Button layout
        button_config = [
            ("C", "⌫", "(", ")", "π"),
            ("sin", "cos", "tan", "√", "x²"),
            ("7", "8", "9", "÷", "x^y"),
            ("4", "5", "6", "×", "n!"),
            ("1", "2", "3", "-", "log"),
            ("0", ".", "±", "+", "=")
        ]

        for i, row in enumerate(button_config):
            buttons_frame.grid_rowconfigure(i, weight=1)
            for j, btn_text in enumerate(row):
                buttons_frame.grid_columnconfigure(j, weight=1)

                btn = tk.Button(
                    buttons_frame,
                    text=btn_text,
                    font=self.custom_font,
                    bg=self.get_button_color(btn_text),
                    fg=self.get_text_color(btn_text),
                    activebackground="#e0e0e0",
                    borderwidth=0,
                    highlightthickness=0,
                    command=lambda x=btn_text: self.on_button_click(x)
                )
                btn.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)

    def get_button_color(self, text):
        if text in {"C", "⌫"}:
            return "#ff9999"
        elif text in {"÷", "×", "-", "+", "="}:
            return "#99ccff"
        elif text in {"sin", "cos", "tan", "√", "x²", "x^y", "n!", "log"}:
            return "#ccffcc"
        else:
            return "#ffffff"

    def get_text_color(self, text):
        if text in {"C", "⌫", "÷", "×", "-", "+", "=", "sin", "cos", "tan", "√", "x²", "x^y", "n!", "log"}:
            return "#000000"
        else:
            return "#000000"

    def on_button_click(self, button_text):
        if button_text == "C":
            self.current_input = ""
            self.total_expression = ""
        elif button_text == "⌫":
            self.current_input = self.current_input[:-1]
        elif button_text == "=":
            self.calculate_result()
        elif button_text == "±":
            if self.current_input and self.current_input[0] == "-":
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
        elif button_text == "π":
            self.current_input = str(3.141592653589793)
        elif button_text in {"sin", "cos", "tan", "√", "x²", "n!", "log"}:
            self.handle_functions(button_text)
        elif button_text == "x^y":
            self.current_input += "**"
        elif button_text in {"÷", "×"}:
            self.current_input += "/" if button_text == "÷" else "*"
        else:
            self.current_input += button_text

        self.update_display()

    def handle_functions(self, func):
        try:
            num = float(self.current_input)
            if func == "sin":
                result = sin(radians(num))
            elif func == "cos":
                result = cos(radians(num))
            elif func == "tan":
                result = tan(radians(num))
            elif func == "√":
                result = sqrt(num)
            elif func == "x²":
                result = num ** 2
            elif func == "n!":
                result = factorial(int(num))
            elif func == "log":
                result = log10(num)

            self.total_expression = f"{func}({self.current_input})"
            self.current_input = str(result)
            self.update_display()
        except:
            self.current_input = "Error"
            self.update_display()

    def calculate_result(self):
        try:
            self.total_expression = self.current_input
            # Replace visual symbols with Python operators
            expression = self.current_input.replace("×", "*").replace("÷", "/")
            result = eval(expression)
            self.current_input = str(result)
        except:
            self.current_input = "Error"
        finally:
            self.update_display()

    def update_display(self):
        self.display_var.set(self.current_input)
        self.history_var.set(self.total_expression)

    def key_press(self, event):
        key = event.char
        keys_mapping = {
            "\r": "=",
            "\x08": "⌫",
            "\x1b": "C",
            "*": "×",
            "/": "÷",
            "^": "x^y"
        }

        if key in keys_mapping:
            self.on_button_click(keys_mapping[key])
        elif key in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-", "(", ")", ".", "p"}:
            btn_text = "π" if key == "p" else key
            self.on_button_click(btn_text)


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()