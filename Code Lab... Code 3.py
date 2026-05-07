import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

# Student Class 
class Student:
    def _init_(self, code, name, cw1, cw2, cw3, exam):
        self.code = int(code)
        self.name = name.strip()
        self.cw = [int(cw1), int(cw2), int(cw3)]
        self.exam = int(exam)

    def total_cw(self):
        return sum(self.cw)

    def total_score(self):
        return self.total_cw() + self.exam

    def percentage(self):
        return (self.total_score() / 160) * 100

    def grade(self):
        p = self.percentage()
        if p >= 70: return 'A'
        elif p >= 60: return 'B'
        elif p >= 50: return 'C'
        elif p >= 40: return 'D'
        else: return 'F'

# File Handling
FILENAME = "studentMarks.txt"

def load_students():
    if not os.path.exists(FILENAME):
        messagebox.showerror("File Error", f"{FILENAME} not found!")
        return []
    with open(FILENAME, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    if not lines:
        return []
    students = []
    try:
        n = int(lines[0])
        for line in lines[1:1+n]:
            parts = line.split(',')
            if len(parts) == 6:
                code, name, c1, c2, c3, exam = parts
                students.append(Student(code, name, c1, c2, c3, exam))
    except Exception as e:
        messagebox.showerror("Load Error", f"Error reading file:\n{e}")
    return students

def save_students(students):
    try:
        with open(FILENAME, 'w') as f:
            f.write(f"{len(students)}\n")
            for s in students:
                f.write(f"{s.code},{s.name},{s.cw[0]},{s.cw[1]},{s.cw[2]},{s.exam}\n")
    except Exception as e:
        messagebox.showerror("Save Error", f"Could not save:\n{e}")

#  Main App 
class StudentManagerApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Student Manager Pro")
        self.root.geometry("1100x780")
        self.root.configure(bg="#f0f7ff")
        self.root.resizable(True, True)

        self.students = load_students()

        self.setup_styles()
        self.create_layout()
        self.update_status(f"Loaded {len(self.students)} students")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Custom beautiful colors
        bg = "#f0f7ff"
        card = "#ffffff"
        accent = "#000000"
        accent_hover = "#3a78c7"
        text = "#2c3e50"
        success = "#27ae60"
        warning = "#e67e22"
        danger = "#e74c3c"

        # Button style
        style.configure("Card.TButton", 
                        font=("Helvetica", 11, "bold"),
                        padding=(20, 12),
                        background=accent,
                        foreground="white")
        style.map("Card.TButton",
                  background=[('active', accent_hover)],
                  foreground=[('active', 'white')])

        # Treeview style
        style.configure("Modern.Treeview",
                        background=card,
                        foreground=text,
                        rowheight=38,
                        fieldbackground=card,
                        font=("Segoe UI", 10))
        style.configure("Modern.Treeview.Heading",
                        font=("Helvetica", 11, "bold"),
                        background=accent,
                        foreground="white")
        style.map("Modern.Treeview",
                  background=[('selected', '#a8d0ff')])

        # Label styles
        style.configure("Title.TLabel", font=("Helvetica", 28, "bold"), foreground=accent, background=bg)
        style.configure("Subtitle.TLabel", font=("Helvetica", 12), foreground="#7f8c8d", background=bg)
        style.configure("Status.TLabel", font=("Segoe UI", 10), foreground="#2ecc71", background="#ecf0f1", padding=10)

    def create_layout(self):
        # Top Header
        header = tk.Frame(self.root, bg="#f0f7ff")
        header.pack(pady=(20, 10), fill=tk.X)

        title = ttk.Label(header, text="Student Manager Pro", style="Title.TLabel")
        title.pack()

        subtitle = ttk.Label(header, text="View • Analyze • Manage Student Performance", style="Subtitle.TLabel")
        subtitle.pack(pady=(5, 20))

        # Main Content Area
        main_container = tk.Frame(self.root, bg="#f0f7ff")
        main_container.pack(fill=tk.BOTH, expand=True, padx=30)

        # Left Panel - Action Buttons (Card Style)
        left_panel = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=1)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        left_panel.pack_propagate(False)
        left_panel.configure(width=300)

        tk.Label(left_panel, text="Actions", font=("Helvetica", 16, "bold"), bg="white", fg="#000000").pack(pady=(25, 15))

        actions = [
            ("All Students", self.view_all),
            ("Search Student", self.view_individual),
            ("Top Performer", self.show_highest),
            ("Lowest Score", self.show_lowest),
            ("Sort Records", self.sort_records),
            ("Add New Student", self.add_student),
            ("Delete Student", self.delete_student),
            ("Update Record", self.update_student),
        ]

        for text, cmd in actions:
            btn = ttk.Button(left_panel, text=text, style="Card.TButton", command=cmd)
            btn.pack(pady=9, padx=25, fill=tk.X)

        # Right Panel - Data Display
        right_panel = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Treeview
        columns = ("Name", "Student ID", "CW Total /60", "Exam /100", "Total /160", "Percentage", "Grade")
        self.tree = ttk.Treeview(right_panel, columns=columns, show="headings", style="Modern.Treeview")

        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.CENTER)
            self.tree.column(col, anchor=tk.CENTER, width=130)
        self.tree.column("Name", width=200, anchor=tk.W)
        self.tree.column("Grade", width=90)

        # Scrollbar
        scrollbar = ttk.Scrollbar(right_panel, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready • System loaded successfully")
        status = ttk.Label(self.root, textvariable=self.status_var, style="Status.TLabel", relief=tk.SUNKEN, anchor=tk.W)
        status.pack(side=tk.BOTTOM, fill=tk.X)

    def update_status(self, msg):
        self.status_var.set(f"Status: {msg}")

    def clear_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

    def display_students(self, stu_list):
        self.clear_tree()
        if not stu_list:
            self.update_status("No students found")
            return

        total_perc = sum(s.percentage() for s in stu_list)
        avg = total_perc / len(stu_list)

        for s in stu_list:
            perc = s.percentage()
            grade = s.grade()
            color = {
                'A': '#27ae60', 'B': '#3498db', 'C': '#f39c12',
                'D': '#e67e22', 'F': '#e74c3c'
            }.get(grade, '#7f8c8d')

            tag = f"grade_{grade}"
            self.tree.tag_configure(tag, foreground=color, font=("Segoe UI", 10, "bold"))

            self.tree.insert("", tk.END, values=(
                s.name,
                s.code,
                s.total_cw(),
                s.exam,
                s.total_score(),
                f"{perc:.1f}%",
                grade
            ), tags=(tag,))

        self.update_status(f"Showing {len(stu_list)} students • Class Average: {avg:.2f}%")

    def view_all(self):
        self.display_students(self.students)

    def find_student(self):
        query = simpledialog.askstring("Search Student", 
                                     "Enter Student ID or Full Name:", parent=self.root)
        if not query: return None
        query = query.strip()

        if query.isdigit():
            code = int(query)
            for s in self.students:
                if s.code == code: return s
        else:
            for s in self.students:
                if s.name.lower() == query.lower(): return s

        messagebox.showwarning("Not Found", "No student found with that name or ID.")
        return None

    def view_individual(self):
        s = self.find_student()
        if s:
            self.clear_tree()
            perc = s.percentage()
            grade = s.grade()
            tag = f"grade_{grade}"
            self.tree.tag_configure(tag, foreground="#27ae60" if grade == 'A' else "#3498db", font=("Segoe UI", 11, "bold"))
            self.tree.insert("", tk.END, values=(
                s.name, s.code, s.total_cw(), s.exam,
                s.total_score(), f"{perc:.1f}%", grade
            ), tags=(tag,))
            self.update_status(f"Found: {s.name} • Grade {grade}")

    def show_highest(self):
        if not self.students:
            messagebox.showinfo("Empty", "No student records.")
            return
        best = max(self.students, key=lambda x: x.percentage())
        self.clear_tree()
        self.tree.insert("", tk.END, values=(
            best.name, best.code, best.total_cw(), best.exam,
            best.total_score(), f"{best.percentage():.1f}%", best.grade()
        ), tags=("highlight",))
        self.tree.tag_configure("highlight", background="#d5f4e6", font=("Segoe UI", 11, "bold"))
        self.update_status(f"Top Student: {best.name} ({best.percentage():.1f}%)")

    def show_lowest(self):
        if not self.students:
            messagebox.showinfo("Empty", "No student records.")
            return
        worst = min(self.students, key=lambda x: x.percentage())
        self.clear_tree()
        self.tree.insert("", tk.END, values=(
            worst.name, worst.code, worst.total_cw(), worst.exam,
            worst.total_score(), f"{worst.percentage():.1f}%", worst.grade()
        ), tags=("low",))
        self.tree.tag_configure("low", background="#fadbd8", font=("Segoe UI", 11, "bold"))
        self.update_status(f"Lowest: {worst.name} ({worst.percentage():.1f}%)")

    def sort_records(self):
        if not self.students: return
        choice = simpledialog.askstring("Sort By", 
            "Choose sort field:\n1. Name\n2. Student ID\n3. Percentage\n\nEnter 1, 2 or 3:", parent=self.root)
        reverse = messagebox.askyesno("Sort Order", "Descending order? (Highest first)", parent=self.root)

        key = {"1": lambda s: s.name.lower(), "2": lambda s: s.code, "3": lambda s: s.percentage()}.get(choice)
        if not key:
            messagebox.showerror("Invalid", "Please enter 1, 2, or 3")
            return

        sorted_list = sorted(self.students, key=key, reverse=reverse)
        self.display_students(sorted_list)

    def add_student(self):
        code = simpledialog.askinteger("Add Student", "Student ID (1000-9999):", minvalue=1000, maxvalue=9999)
        if not code or any(s.code == code for s in self.students):
            messagebox.showerror("Error", "Invalid or duplicate ID!")
            return
        name = simpledialog.askstring("Add Student", "Full Name:")
        if not name or not name.strip(): return

        def ask(prompt, mx):
            while True:
                val = simpledialog.askinteger("Input", prompt, minvalue=0, maxvalue=mx)
                if val is not None: return val
                if messagebox.askyesno("Cancel", "Cancel adding student?"): return None

        cw = [ask(f"Coursework {i} (0-20):", 20) for i in range(1,4)]
        if None in cw: return
        exam = ask("Exam Mark (0-100):", 100)
        if exam is None: return

        self.students.append(Student(code, name, *cw, exam))
        save_students(self.students)
        self.update_status(f"Added: {name}")
        messagebox.showinfo("Success", f"Student '{name}' added successfully!")

    def delete_student(self):
        s = self.find_student()
        if not s: return
        if messagebox.askyesno("Confirm Delete", f"Permanently delete {s.name} ({s.code})?"):
            self.students.remove(s)
            save_students(self.students)
            self.update_status(f"Deleted: {s.name}")
            messagebox.showinfo("Deleted", "Student record removed.")

    def update_student(self):
        s = self.find_student()
        if not s: return

        fields = ["Name", "Coursework 1", "Coursework 2", "Coursework 3", "Exam Mark"]
        choice = simpledialog.askstring("Update", 
            "Select field to update:\n" + "\n".join(f"{i+1}. {f}" for i, f in enumerate(fields)))

        if not choice or not choice.isdigit() or int(choice) not in range(1, 6):
            return
        idx = int(choice) - 1

        if idx == 0:
            new = simpledialog.askstring("Update Name", "New name:", initialvalue=s.name)
            if new: s.name = new.strip()
        elif idx <= 3:
            new = simpledialog.askinteger("Update", f"New Coursework {idx} (0-20):", minvalue=0, maxvalue=20)
            if new is not None: s.cw[idx-1] = new
        else:
            new = simpledialog.askinteger("Update", "New Exam Mark (0-100):", minvalue=0, maxvalue=100)
            if new is not None: s.exam = new

        save_students(self.students)
        self.update_status(f"Updated: {s.name}")
        messagebox.showinfo("Updated", "Student record updated!")

# ====================== Launch App ======================
if _name_ == "_main_":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()