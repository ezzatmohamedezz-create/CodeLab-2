import tkinter as tk
from tkinter import ttk
import random

# Built-in jokes  no file needed
JOKES = [
    {"setup": "Why don't skeletons fight each other?", "punchline": "They don't have the guts!"},
    {"setup": "What do you call fake spaghetti?", "punchline": "An impasta!"},
    {"setup": "Why did the scarecrow win an award?", "punchline": "Because he was outstanding in his field!"},
    {"setup": "Why don't eggs tell jokes?", "punchline": "They'd crack each other up!"},
    {"setup": "What do you call cheese that isn't yours?", "punchline": "Nacho cheese!"},
    {"setup": "Why couldn't the bicycle stand up?", "punchline": "It was two-tired!"},
    {"setup": "How does a penguin build its house?", "punchline": "Igloos it together!"},
    {"setup": "What did one wall say to the other?", "punchline": "I'll meet you at the corner!"}
]

class JokeApp:
    def _init_(self):
        self.root = tk.Tk()
        self.root.title("Alexa Joke Master")
        self.root.geometry("800x700")
        self.root.configure(bg="#0f172a")
        self.root.resizable(False, False)

        # Title
        tk.Label(self.root, text="Alexa Joke Master", font=("Arial", 34, "bold"), 
                 bg="#0f172a", fg="#22d3ee").pack(pady=30)

        # Big Alexa button
        self.alexa_btn = tk.Button(self.root, text="Alexa,\nTell me a joke!", 
                 font=("Arial", 20, "bold"), bg="#22d3ee", fg="black",
                 activebackground="#67e8f9", relief="flat", cursor="hand2",
                 command=self.tell_joke, height=3, width=20)
        self.alexa_btn.pack(pady=40)

        # Joke card
        card = tk.Frame(self.root, bg="#1e293b", relief="raised", bd=8)
        card.pack(pady=20, padx=60, fill="both", expand=True)

        self.setup_label = tk.Label(card, text="Click the button to hear a joke!", 
                     font=("Arial", 20, "bold"), bg="#1e293b", fg="#a5f3fc",
                     wraplength=650, justify="center")
        self.setup_label.pack(pady=40)

        self.punchline_label = tk.Label(card, text="", 
                     font=("Arial", 26, "italic"), bg="#1e293b", fg="#f472b6",
                     wraplength=650, justify="center")
        self.punchline_label.pack(pady=20)

        # Bottom buttons BIG AND VISIBLE
        btn_frame = tk.Frame(self.root, bg="#0f172a")
        btn_frame.pack(pady=30)

        self.show_btn = tk.Button(btn_frame, text="Show Punchline", font=("Arial", 16, "bold"),
                                  bg="#f472b6", fg="white", width=18, height=2,
                                  command=self.show_punchline, state="disabled")
        self.show_btn.pack(side="left", padx=30)

        tk.Button(btn_frame, text="Next Joke", font=("Arial", 16, "bold"),
                  bg="#22d3ee", fg="black", width=18, height=2,
                  command=self.next_joke).pack(side="left", padx=30)

        tk.Button(btn_frame, text="Quit", font=("Arial", 16, "bold"),
                  bg="#64748b", fg="white", width=18, height=2,
                  command=self.root.destroy).pack(side="left", padx=30)

        self.current_joke = None

    def tell_joke(self):
        self.current_joke = random.choice(JOKES)
        self.setup_label.config(text=self.current_joke["setup"])
        self.punchline_label.config(text="")
        self.show_btn.config(state="normal")

        # Flash effect
        original = self.alexa_btn["bg"]
        self.alexa_btn.config(bg="#f59e0b")
        self.root.after(200, lambda: self.alexa_btn.config(bg=original))

    def show_punchline(self):
        if self.current_joke:
            self.punchline_label.config(text=self.current_joke["punchline"])
            self.show_btn.config(state="disabled")

    def next_joke(self):
        self.punchline_label.config(text="")
        self.show_btn.config(state="disabled")
        self.tell_joke()

    def run(self):
        self.root.mainloop()

# run
if _name_ == "_main_":
    app = JokeApp()
    app.run()