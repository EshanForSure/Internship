
import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip
import re
from datetime import datetime

class PasswordGenerator:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Password Generator")
        self.root.geometry("900x500")
        self.root.configure(bg="#2c3e50")
        self.root.resizable(False, False)

        # Password history
        self.password_history = []

        # Character sets
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.ambiguous = "0O1l"

        self.setup_gui()

    def setup_gui(self):
        # Title
        title_label = tk.Label(self.root,
                               text="🔒 Password Generator",
                               font=("Arial", 18, "bold"),
                               bg="#2c3e50",
                               fg="#ecf0f1")
        title_label.pack(pady=10)

        # Main container with two columns
        main_container = tk.Frame(self.root, bg="#2c3e50")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Left column frame
        left_frame = tk.Frame(main_container, bg="#2c3e50")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Right column frame
        right_frame = tk.Frame(main_container, bg="#2c3e50")
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # LEFT COLUMN CONTENT

        # Password length section
        length_frame = tk.LabelFrame(left_frame,
                                     text="Password Length",
                                     font=("Arial", 10, "bold"),
                                     bg="#34495e",
                                     fg="#ecf0f1",
                                     bd=2)
        length_frame.pack(fill="x", pady=5)

        tk.Label(length_frame,
                 text="Length:",
                 bg="#34495e",
                 fg="#ecf0f1",
                 font=("Arial", 10)).pack(side="left", padx=5)

        self.length_var = tk.StringVar(value="12")
        self.length_scale = tk.Scale(length_frame,
                                     from_=4,
                                     to=128,
                                     orient="horizontal",
                                     variable=self.length_var,
                                     bg="#34495e",
                                     fg="#ecf0f1",
                                     highlightbackground="#34495e")
        self.length_scale.pack(side="left", fill="x", expand=True, padx=5)

        self.length_entry = tk.Entry(length_frame,
                                     textvariable=self.length_var,
                                     width=5,
                                     font=("Arial", 10))
        self.length_entry.pack(side="right", padx=5)

        # Character options section
        options_frame = tk.LabelFrame(left_frame,
                                      text="Character Options",
                                      font=("Arial", 10, "bold"),
                                      bg="#34495e",
                                      fg="#ecf0f1",
                                      bd=2)
        options_frame.pack(fill="x", pady=5)

        self.lowercase_var = tk.BooleanVar(value=True)
        self.uppercase_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.exclude_ambiguous_var = tk.BooleanVar(value=False)

        tk.Checkbutton(options_frame,
                       text="Lowercase (a-z)",
                       variable=self.lowercase_var,
                       bg="#34495e",
                       fg="#ecf0f1",
                       selectcolor="#2c3e50",
                       font=("Arial", 9)).pack(anchor="w", padx=5)

        tk.Checkbutton(options_frame,
                       text="Uppercase (A-Z)",
                       variable=self.uppercase_var,
                       bg="#34495e",
                       fg="#ecf0f1",
                       selectcolor="#2c3e50",
                       font=("Arial", 9)).pack(anchor="w", padx=5)

        tk.Checkbutton(options_frame,
                       text="Numbers (0-9)",
                       variable=self.digits_var,
                       bg="#34495e",
                       fg="#ecf0f1",
                       selectcolor="#2c3e50",
                       font=("Arial", 9)).pack(anchor="w", padx=5)

        tk.Checkbutton(options_frame,
                       text="Symbols (!@#$%^&*)",
                       variable=self.symbols_var,
                       bg="#34495e",
                       fg="#ecf0f1",
                       selectcolor="#2c3e50",
                       font=("Arial", 9)).pack(anchor="w", padx=5)

        tk.Checkbutton(options_frame,
                       text="Exclude Ambiguous (0, O, 1, l)",
                       variable=self.exclude_ambiguous_var,
                       bg="#34495e",
                       fg="#ecf0f1",
                       selectcolor="#2c3e50",
                       font=("Arial", 9)).pack(anchor="w", padx=5)

        # Custom characters section
        custom_frame = tk.LabelFrame(left_frame,
                                     text="Custom Characters",
                                     font=("Arial", 10, "bold"),
                                     bg="#34495e",
                                     fg="#ecf0f1",
                                     bd=2)
        custom_frame.pack(fill="x", pady=5)

        tk.Label(custom_frame,
                 text="Include:",
                 bg="#34495e",
                 fg="#ecf0f1",
                 font=("Arial", 9)).pack(anchor="w", padx=5)

        self.custom_include = tk.Entry(custom_frame,
                                       font=("Arial", 9),
                                       width=30)
        self.custom_include.pack(fill="x", padx=5, pady=2)

        tk.Label(custom_frame,
                 text="Exclude:",
                 bg="#34495e",
                 fg="#ecf0f1",
                 font=("Arial", 9)).pack(anchor="w", padx=5)

        self.custom_exclude = tk.Entry(custom_frame,
                                       font=("Arial", 9),
                                       width=30)
        self.custom_exclude.pack(fill="x", padx=5, pady=2)

        # RIGHT COLUMN CONTENT

        # Security rules section
        security_frame = tk.LabelFrame(right_frame,
                                       text="Security Rules",
                                       font=("Arial", 10, "bold"),
                                       bg="#34495e",
                                       fg="#ecf0f1",
                                       bd=2)
        security_frame.pack(fill="x", pady=5)

        self.no_repeating_var = tk.BooleanVar(value=False)
        self.no_sequential_var = tk.BooleanVar(value=False)
        self.min_each_type_var = tk.BooleanVar(value=True)

        tk.Checkbutton(security_frame,
                       text="No repeating characters",
                       variable=self.no_repeating_var,
                       bg="#34495e",
                       fg="#ecf0f1",
                       selectcolor="#2c3e50",
                       font=("Arial", 9)).pack(anchor="w", padx=5)

        tk.Checkbutton(security_frame,
                       text="No sequential characters (abc, 123)",
                       variable=self.no_sequential_var,
                       bg="#34495e",
                       fg="#ecf0f1",
                       selectcolor="#2c3e50",
                       font=("Arial", 9)).pack(anchor="w", padx=5)

        tk.Checkbutton(security_frame,
                       text="Minimum 1 of each selected type",
                       variable=self.min_each_type_var,
                       bg="#34495e",
                       fg="#ecf0f1",
                       selectcolor="#2c3e50",
                       font=("Arial", 9)).pack(anchor="w", padx=5)

        # Generate button
        generate_btn = tk.Button(right_frame,
                                 text="🔑 Generate Password",
                                 command=self.generate_password,
                                 bg="#e74c3c",
                                 fg="white",
                                 font=("Arial", 12, "bold"),
                                 relief="raised",
                                 bd=3,
                                 padx=20,
                                 pady=10)
        generate_btn.pack(pady=10)

        # Generated password section
        password_frame = tk.LabelFrame(right_frame,
                                       text="Generated Password",
                                       font=("Arial", 10, "bold"),
                                       bg="#34495e",
                                       fg="#ecf0f1",
                                       bd=2)
        password_frame.pack(fill="x", pady=5)

        self.password_text = tk.Text(password_frame,
                                     height=3,
                                     font=("Courier", 12),
                                     wrap="word")
        self.password_text.pack(fill="x", padx=5, pady=5)

        # Buttons frame
        buttons_frame = tk.Frame(password_frame, bg="#34495e")
        buttons_frame.pack(fill="x", padx=5, pady=5)

        copy_btn = tk.Button(buttons_frame,
                             text="📋 Copy",
                             command=self.copy_password,
                             bg="#3498db",
                             fg="white",
                             font=("Arial", 9, "bold"))
        copy_btn.pack(side="left", padx=5)

        strength_btn = tk.Button(buttons_frame,
                                 text="🛡️ Check Strength",
                                 command=self.check_strength,
                                 bg="#f39c12",
                                 fg="white",
                                 font=("Arial", 9, "bold"))
        strength_btn.pack(side="left", padx=5)

        history_btn = tk.Button(buttons_frame,
                                text="📚 View History",
                                command=self.show_history,
                                bg="#9b59b6",
                                fg="white",
                                font=("Arial", 9, "bold"))
        history_btn.pack(side="left", padx=5)

        # Strength indicator
        self.strength_label = tk.Label(
            password_frame,
            text="Password strength will appear here",
            bg="#34495e",
            fg="#ecf0f1",
            font=("Arial", 9))
        self.strength_label.pack(pady=5)

    def generate_password(self):
        try:
            length = int(self.length_var.get())
            if length < 4 or length > 128:
                messagebox.showerror(
                    "Error", "Password length must be between 4 and 128")
                return
        except ValueError:
            messagebox.showerror("Error",
                                 "Please enter a valid password length")
            return

        # Build character set
        char_set = ""
        required_chars = []

        if self.lowercase_var.get():
            chars = self.lowercase
            if self.exclude_ambiguous_var.get():
                chars = ''.join(c for c in chars if c not in self.ambiguous)
            char_set += chars
            if self.min_each_type_var.get():
                required_chars.append(random.choice(chars))

        if self.uppercase_var.get():
            chars = self.uppercase
            if self.exclude_ambiguous_var.get():
                chars = ''.join(c for c in chars if c not in self.ambiguous)
            char_set += chars
            if self.min_each_type_var.get():
                required_chars.append(random.choice(chars))

        if self.digits_var.get():
            chars = self.digits
            if self.exclude_ambiguous_var.get():
                chars = ''.join(c for c in chars if c not in self.ambiguous)
            char_set += chars
            if self.min_each_type_var.get():
                required_chars.append(random.choice(chars))

        if self.symbols_var.get():
            char_set += self.symbols
            if self.min_each_type_var.get():
                required_chars.append(random.choice(self.symbols))

        # Add custom characters
        if self.custom_include.get():
            char_set += self.custom_include.get()

        # Remove excluded characters
        if self.custom_exclude.get():
            for char in self.custom_exclude.get():
                char_set = char_set.replace(char, '')

        if not char_set:
            messagebox.showerror("Error", "No character types selected!")
            return

        # Generate password with security rules
        max_attempts = 1000
        for attempt in range(max_attempts):
            password = self._generate_single_password(char_set, length,
                                                      required_chars)

            if self._validate_password(password):
                break
        else:
            messagebox.showwarning(
                "Warning",
                "Could not generate password meeting all security rules. Relaxing constraints..."
            )
            password = self._generate_single_password(char_set, length,
                                                      required_chars)

        # Display password
        self.password_text.delete(1.0, tk.END)
        self.password_text.insert(tk.END, password)

        # Add to history
        self.password_history.append({
            'password':
            password,
            'timestamp':
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'length':
            length
        })

        # Keep only last 10 passwords
        if len(self.password_history) > 10:
            self.password_history.pop(0)

        # Check strength automatically
        self.check_strength()

    def _generate_single_password(self, char_set, length, required_chars):
        password = list(required_chars)
        remaining_length = length - len(required_chars)

        for _ in range(remaining_length):
            password.append(random.choice(char_set))

        random.shuffle(password)
        return ''.join(password)

    def _validate_password(self, password):
        # Check no repeating characters
        if self.no_repeating_var.get():
            if len(set(password)) != len(password):
                return False

        # Check no sequential characters
        if self.no_sequential_var.get():
            for i in range(len(password) - 2):
                # Check for sequential ASCII values
                if (ord(password[i]) + 1 == ord(password[i + 1])
                        and ord(password[i + 1]) + 1 == ord(password[i + 2])):
                    return False

        return True

    def copy_password(self):
        password = self.password_text.get(1.0, tk.END).strip()
        if password:
            try:
                pyperclip.copy(password)
                messagebox.showinfo("Success", "Password copied to clipboard!")
            except:
                messagebox.showerror("Error", "Could not copy to clipboard")
        else:
            messagebox.showwarning("Warning", "No password to copy!")

    def check_strength(self):
        password = self.password_text.get(1.0, tk.END).strip()
        if not password:
            self.strength_label.config(text="No password to check",
                                       fg="#e74c3c")
            return

        score = 0
        feedback = []

        # Length check
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
        else:
            feedback.append("Too short")

        # Character variety
        if re.search(r'[a-z]', password):
            score += 1
        else:
            feedback.append("Add lowercase")

        if re.search(r'[A-Z]', password):
            score += 1
        else:
            feedback.append("Add uppercase")

        if re.search(r'\d', password):
            score += 1
        else:
            feedback.append("Add numbers")

        if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            score += 2
        else:
            feedback.append("Add symbols")

        # No common patterns
        if not re.search(r'(.)\1{2,}', password):
            score += 1
        else:
            feedback.append("Avoid repetition")

        # Strength assessment
        if score >= 7:
            strength = "Very Strong 🛡️"
            color = "#27ae60"
        elif score >= 5:
            strength = "Strong 💪"
            color = "#f39c12"
        elif score >= 3:
            strength = "Moderate ⚠️"
            color = "#e67e22"
        else:
            strength = "Weak ❌"
            color = "#e74c3c"

        result = f"Strength: {strength} (Score: {score}/8)"
        if feedback:
            result += f"\nSuggestions: {', '.join(feedback)}"

        self.strength_label.config(text=result, fg=color)

    def show_history(self):
        if not self.password_history:
            messagebox.showinfo("History", "No passwords generated yet!")
            return

        history_window = tk.Toplevel(self.root)
        history_window.title("Password History")
        history_window.geometry("600x400")
        history_window.configure(bg="#2c3e50")

        # Create listbox with scrollbar
        frame = tk.Frame(history_window, bg="#2c3e50")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(frame,
                             yscrollcommand=scrollbar.set,
                             font=("Courier", 10),
                             bg="#34495e",
                             fg="#ecf0f1")
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        # Populate history
        for i, entry in enumerate(reversed(self.password_history)):
            item = f"{entry['timestamp']} | Length: {entry['length']} | {entry['password']}"
            listbox.insert(tk.END, item)

        # Copy selected password function
        def copy_selected():
            selection = listbox.curselection()
            if selection:
                item = listbox.get(selection[0])
                password = item.split(" | ")[-1]
                try:
                    pyperclip.copy(password)
                    messagebox.showinfo("Success",
                                        "Password copied to clipboard!")
                except:
                    messagebox.showerror("Error",
                                         "Could not copy to clipboard")

        copy_btn = tk.Button(history_window,
                             text="Copy Selected Password",
                             command=copy_selected,
                             bg="#3498db",
                             fg="white",
                             font=("Arial", 10, "bold"))
        copy_btn.pack(pady=5)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    try:
        import pyperclip
    except ImportError:
        print("Installing pyperclip for clipboard functionality...")
        import subprocess
        subprocess.run(["python", "-m", "pip", "install", "pyperclip"],
                       check=True)
        import pyperclip

    app = PasswordGenerator()
    app.run()


import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip
import re
from datetime import datetime


class PasswordGenerator:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Password Generator")
        self.root.geometry("900x500")
        self.root.configure(bg="#2c3e50")
        self.root.resizable(False, False)

        # Password history
        self.password_history = []

        # Character sets
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.ambiguous = "0O1l"

        self.setup_gui()

    def setup_gui(self):
        # Title
        title_label = tk.Label(self.root,
                               text="🔒 Password Generator",
                               font=("Arial", 18, "bold"),
                               bg="#2c3e50",
                               fg="#ecf0f1")
        title_label.pack(pady=10)

        # Main container with two columns
        main_container = tk.Frame(self.root, bg="#2c3e50")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Left column frame
        left_frame = tk.Frame(main_container, bg="#2c3e50")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Right column frame
        right_frame = tk.Frame(main_container, bg="#2c3e50")
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # LEFT COLUMN CONTENT

        # Password length section
        length_frame = tk.LabelFrame(left_frame,
                                     text="Password Length",
                                     font=("Arial", 10, "bold"),
                                     bg="#34495e",
                                     fg="#ecf0f1",
                                     bd=2)
        length_frame.pack(fill="x", pady=5)

        tk.Label(length_frame,
                 text="Length:",
                 bg="#34495e",
                 fg="#ecf0f1",
                 font=("Arial", 10)).pack(side="left", padx=5)

        self.length_var = tk.StringVar(value="12")
        self.length_scale = tk.Scale(length_frame,
                                     from_=4,
                                     to=128,
                                     orient="horizontal",
                                     variable=self.length_var,
                                     bg="#34495e",
                                     fg="#ecf0f1",
                                     highlightbackground="#34495e")
        self.length_scale.pack(side="left", fill="x", expand=True, padx=5)

        self.length_entry = tk.Entry(length_frame,
                                     textvariable=self.length_var,
                                     width=5,
                                     font=("Arial", 10))
        self.length_entry.pack(side="right", padx=5)

        # Character options section
        options_frame = tk.LabelFrame(left_frame,
                                      text="Character Options",
                                      font=("Arial", 10, "bold"),
                                      bg="#34495e",
                                      fg="#ecf0f1",
                                      bd=2)
        options_frame.pack(fill="x", pady=5)

        self.lowercase_var = tk.BooleanVar(value=True)
        self.uppercase_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.exclude_ambiguous_var = tk.BooleanVar(value=False)

        tk.Checkbutton(options_frame,
                       text="Lowercase (a-z)",
                       variable=self.lowercase_var,
                       bg="#34495e",
                       fg="#ecf0f1",
                       selectcolor="#2c3e50",
                       font=("Arial", 9)).pack(anchor="w", padx=5)

        tk.Checkbutton(options_frame,
                       text="Uppercase (A-Z)",
                       variable=self.uppercase_var,
                       bg="#34495e",
                       fg="#ecf0f1",
                       selectcolor="#2c3e50",
                       font=("Arial", 9)).pack(anchor="w", padx=5)

        tk.Checkbutton(options_frame,
                       text="Numbers (0-9)",
                       variable=self.digits_var,
                       bg="#34495e",
                       fg="#ecf0f1",
                       selectcolor="#2c3e50",
                       font=("Arial", 9)).pack(anchor="w", padx=5)

        tk.Checkbutton(options_frame,
                       text="Symbols (!@#$%^&*)",
                       variable=self.symbols_var,
                       bg="#34495e",
                       fg="#ecf0f1",
                       selectcolor="#2c3e50",
                       font=("Arial", 9)).pack(anchor="w", padx=5)

        tk.Checkbutton(options_frame,
                       text="Exclude Ambiguous (0, O, 1, l)",
                       variable=self.exclude_ambiguous_var,
                       bg="#34495e",
                       fg="#ecf0f1",
                       selectcolor="#2c3e50",
                       font=("Arial", 9)).pack(anchor="w", padx=5)

        # Custom characters section
        custom_frame = tk.LabelFrame(left_frame,
                                     text="Custom Characters",
                                     font=("Arial", 10, "bold"),
                                     bg="#34495e",
                                     fg="#ecf0f1",
                                     bd=2)
        custom_frame.pack(fill="x", pady=5)

        tk.Label(custom_frame,
                 text="Include:",
                 bg="#34495e",
                 fg="#ecf0f1",
                 font=("Arial", 9)).pack(anchor="w", padx=5)

        self.custom_include = tk.Entry(custom_frame,
                                       font=("Arial", 9),
                                       width=30)
        self.custom_include.pack(fill="x", padx=5, pady=2)

        tk.Label(custom_frame,
                 text="Exclude:",
                 bg="#34495e",
                 fg="#ecf0f1",
                 font=("Arial", 9)).pack(anchor="w", padx=5)

        self.custom_exclude = tk.Entry(custom_frame,
                                       font=("Arial", 9),
                                       width=30)
        self.custom_exclude.pack(fill="x", padx=5, pady=2)

        # RIGHT COLUMN CONTENT

        # Security rules section
        security_frame = tk.LabelFrame(right_frame,
                                       text="Security Rules",
                                       font=("Arial", 10, "bold"),
                                       bg="#34495e",
                                       fg="#ecf0f1",
                                       bd=2)
        security_frame.pack(fill="x", pady=5)

        self.no_repeating_var = tk.BooleanVar(value=False)
        self.no_sequential_var = tk.BooleanVar(value=False)
        self.min_each_type_var = tk.BooleanVar(value=True)

        tk.Checkbutton(security_frame,
                       text="No repeating characters",
                       variable=self.no_repeating_var,
                       bg="#34495e",
                       fg="#ecf0f1",
                       selectcolor="#2c3e50",
                       font=("Arial", 9)).pack(anchor="w", padx=5)

        tk.Checkbutton(security_frame,
                       text="No sequential characters (abc, 123)",
                       variable=self.no_sequential_var,
                       bg="#34495e",
                       fg="#ecf0f1",
                       selectcolor="#2c3e50",
                       font=("Arial", 9)).pack(anchor="w", padx=5)

        tk.Checkbutton(security_frame,
                       text="Minimum 1 of each selected type",
                       variable=self.min_each_type_var,
                       bg="#34495e",
                       fg="#ecf0f1",
                       selectcolor="#2c3e50",
                       font=("Arial", 9)).pack(anchor="w", padx=5)

        # Generate button
        generate_btn = tk.Button(right_frame,
                                 text="🔑 Generate Password",
                                 command=self.generate_password,
                                 bg="#e74c3c",
                                 fg="white",
                                 font=("Arial", 12, "bold"),
                                 relief="raised",
                                 bd=3,
                                 padx=20,
                                 pady=10)
        generate_btn.pack(pady=10)

        # Generated password section
        password_frame = tk.LabelFrame(right_frame,
                                       text="Generated Password",
                                       font=("Arial", 10, "bold"),
                                       bg="#34495e",
                                       fg="#ecf0f1",
                                       bd=2)
        password_frame.pack(fill="x", pady=5)

        self.password_text = tk.Text(password_frame,
                                     height=3,
                                     font=("Courier", 12),
                                     wrap="word")
        self.password_text.pack(fill="x", padx=5, pady=5)

        # Buttons frame
        buttons_frame = tk.Frame(password_frame, bg="#34495e")
        buttons_frame.pack(fill="x", padx=5, pady=5)

        copy_btn = tk.Button(buttons_frame,
                             text="📋 Copy",
                             command=self.copy_password,
                             bg="#3498db",
                             fg="white",
                             font=("Arial", 9, "bold"))
        copy_btn.pack(side="left", padx=5)

        strength_btn = tk.Button(buttons_frame,
                                 text="🛡️ Check Strength",
                                 command=self.check_strength,
                                 bg="#f39c12",
                                 fg="white",
                                 font=("Arial", 9, "bold"))
        strength_btn.pack(side="left", padx=5)

        history_btn = tk.Button(buttons_frame,
                                text="📚 View History",
                                command=self.show_history,
                                bg="#9b59b6",
                                fg="white",
                                font=("Arial", 9, "bold"))
        history_btn.pack(side="left", padx=5)

        # Strength indicator
        self.strength_label = tk.Label(
            password_frame,
            text="Password strength will appear here",
            bg="#34495e",
            fg="#ecf0f1",
            font=("Arial", 9))
        self.strength_label.pack(pady=5)

    def generate_password(self):
        try:
            length = int(self.length_var.get())
            if length < 4 or length > 128:
                messagebox.showerror(
                    "Error", "Password length must be between 4 and 128")
                return
        except ValueError:
            messagebox.showerror("Error",
                                 "Please enter a valid password length")
            return

        # Build character set
        char_set = ""
        required_chars = []

        if self.lowercase_var.get():
            chars = self.lowercase
            if self.exclude_ambiguous_var.get():
                chars = ''.join(c for c in chars if c not in self.ambiguous)
            char_set += chars
            if self.min_each_type_var.get():
                required_chars.append(random.choice(chars))

        if self.uppercase_var.get():
            chars = self.uppercase
            if self.exclude_ambiguous_var.get():
                chars = ''.join(c for c in chars if c not in self.ambiguous)
            char_set += chars
            if self.min_each_type_var.get():
                required_chars.append(random.choice(chars))

        if self.digits_var.get():
            chars = self.digits
            if self.exclude_ambiguous_var.get():
                chars = ''.join(c for c in chars if c not in self.ambiguous)
            char_set += chars
            if self.min_each_type_var.get():
                required_chars.append(random.choice(chars))

        if self.symbols_var.get():
            char_set += self.symbols
            if self.min_each_type_var.get():
                required_chars.append(random.choice(self.symbols))

        # Add custom characters
        if self.custom_include.get():
            char_set += self.custom_include.get()

        # Remove excluded characters
        if self.custom_exclude.get():
            for char in self.custom_exclude.get():
                char_set = char_set.replace(char, '')

        if not char_set:
            messagebox.showerror("Error", "No character types selected!")
            return

        # Generate password with security rules
        max_attempts = 1000
        for attempt in range(max_attempts):
            password = self._generate_single_password(char_set, length,
                                                      required_chars)

            if self._validate_password(password):
                break
        else:
            messagebox.showwarning(
                "Warning",
                "Could not generate password meeting all security rules. Relaxing constraints..."
            )
            password = self._generate_single_password(char_set, length,
                                                      required_chars)

        # Display password
        self.password_text.delete(1.0, tk.END)
        self.password_text.insert(tk.END, password)

        # Add to history
        self.password_history.append({
            'password':
            password,
            'timestamp':
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'length':
            length
        })

        # Keep only last 10 passwords
        if len(self.password_history) > 10:
            self.password_history.pop(0)

        # Check strength automatically
        self.check_strength()

    def _generate_single_password(self, char_set, length, required_chars):
        password = list(required_chars)
        remaining_length = length - len(required_chars)

        for _ in range(remaining_length):
            password.append(random.choice(char_set))

        random.shuffle(password)
        return ''.join(password)

    def _validate_password(self, password):
        # Check no repeating characters
        if self.no_repeating_var.get():
            if len(set(password)) != len(password):
                return False

        # Check no sequential characters
        if self.no_sequential_var.get():
            for i in range(len(password) - 2):
                # Check for sequential ASCII values
                if (ord(password[i]) + 1 == ord(password[i + 1])
                        and ord(password[i + 1]) + 1 == ord(password[i + 2])):
                    return False

        return True

    def copy_password(self):
        password = self.password_text.get(1.0, tk.END).strip()
        if password:
            try:
                pyperclip.copy(password)
                messagebox.showinfo("Success", "Password copied to clipboard!")
            except:
                messagebox.showerror("Error", "Could not copy to clipboard")
        else:
            messagebox.showwarning("Warning", "No password to copy!")

    def check_strength(self):
        password = self.password_text.get(1.0, tk.END).strip()
        if not password:
            self.strength_label.config(text="No password to check",
                                       fg="#e74c3c")
            return

        score = 0
        feedback = []

        # Length check
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
        else:
            feedback.append("Too short")

        # Character variety
        if re.search(r'[a-z]', password):
            score += 1
        else:
            feedback.append("Add lowercase")

        if re.search(r'[A-Z]', password):
            score += 1
        else:
            feedback.append("Add uppercase")

        if re.search(r'\d', password):
            score += 1
        else:
            feedback.append("Add numbers")

        if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            score += 2
        else:
            feedback.append("Add symbols")

        # No common patterns
        if not re.search(r'(.)\1{2,}', password):
            score += 1
        else:
            feedback.append("Avoid repetition")

        # Strength assessment
        if score >= 7:
            strength = "Very Strong 🛡️"
            color = "#27ae60"
        elif score >= 5:
            strength = "Strong 💪"
            color = "#f39c12"
        elif score >= 3:
            strength = "Moderate ⚠️"
            color = "#e67e22"
        else:
            strength = "Weak ❌"
            color = "#e74c3c"

        result = f"Strength: {strength} (Score: {score}/8)"
        if feedback:
            result += f"\nSuggestions: {', '.join(feedback)}"

        self.strength_label.config(text=result, fg=color)

    def show_history(self):
        if not self.password_history:
            messagebox.showinfo("History", "No passwords generated yet!")
            return

        history_window = tk.Toplevel(self.root)
        history_window.title("Password History")
        history_window.geometry("600x400")
        history_window.configure(bg="#2c3e50")

        # Create listbox with scrollbar
        frame = tk.Frame(history_window, bg="#2c3e50")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(frame,
                             yscrollcommand=scrollbar.set,
                             font=("Courier", 10),
                             bg="#34495e",
                             fg="#ecf0f1")
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        # Populate history
        for i, entry in enumerate(reversed(self.password_history)):
            item = f"{entry['timestamp']} | Length: {entry['length']} | {entry['password']}"
            listbox.insert(tk.END, item)

        # Copy selected password function
        def copy_selected():
            selection = listbox.curselection()
            if selection:
                item = listbox.get(selection[0])
                password = item.split(" | ")[-1]
                try:
                    pyperclip.copy(password)
                    messagebox.showinfo("Success",
                                        "Password copied to clipboard!")
                except:
                    messagebox.showerror("Error",
                                         "Could not copy to clipboard")

        copy_btn = tk.Button(history_window,
                             text="Copy Selected Password",
                             command=copy_selected,
                             bg="#3498db",
                             fg="white",
                             font=("Arial", 10, "bold"))
        copy_btn.pack(pady=5)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    try:
        import pyperclip
    except ImportError:
        print("Installing pyperclip for clipboard functionality...")
        import subprocess
        subprocess.run(["python", "-m", "pip", "install", "pyperclip"],
                       check=True)
        import pyperclip

    app = PasswordGenerator()
    app.run()
