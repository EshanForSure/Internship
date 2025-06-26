# Example: Tkinter GUI outline
import tkinter as tk
from tkinter import messagebox
import sqlite3
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import os
#hello
data_file = "bmi_data.db"


def calculate_bmi(weight, height):
    return weight / (height**2)


def get_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 24.9:
        return "Normal"
    elif bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"


def save_data(user, bmi_record):
    # Create database and table if they don't exist
    conn = sqlite3.connect(data_file)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bmi_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            date DATE NOT NULL,
            weight REAL NOT NULL,
            height REAL NOT NULL,
            bmi REAL NOT NULL,
            category TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert new record
    cursor.execute('''
        INSERT INTO bmi_records (user, date, weight, height, bmi, category)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user, bmi_record['date'], bmi_record['weight'], 
          bmi_record['height'], bmi_record['bmi'], bmi_record['category']))
    
    conn.commit()
    conn.close()


def view_all_data():
    try:
        conn = sqlite3.connect(data_file)
        df = pd.read_sql_query("SELECT * FROM bmi_records ORDER BY date, created_at", conn)
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Database error: {str(e)}")
        return
    except Exception as e:
        messagebox.showerror("Error", f"No data found: {str(e)}")
        return

    if df.empty:
        messagebox.showinfo("Info", "No BMI data found in database.")
        return

    # Create a formatted string of all data
    data_text = "🗃️ All BMI Records in Database:\n\n"
    
    for _, row in df.iterrows():
        data_text += f"ID: {row['id']} | User: {row['user']}\n"
        data_text += f"Date: {row['date']} | Weight: {row['weight']}kg | Height: {row['height']}m\n"
        data_text += f"BMI: {row['bmi']} | Category: {row['category']}\n"
        data_text += f"Created: {row['created_at']}\n"
        data_text += "-" * 50 + "\n"
    
    # Create a new window to display the data
    data_window = tk.Toplevel(root)
    data_window.title("Database Records")
    data_window.geometry("600x400")
    data_window.configure(bg="#2c3e50")
    
    # Add scrollable text widget
    text_frame = tk.Frame(data_window, bg="#2c3e50")
    text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    text_widget = tk.Text(text_frame, 
                         yscrollcommand=scrollbar.set,
                         bg="#ecf0f1", 
                         fg="#2c3e50",
                         font=("Courier", 10),
                         wrap=tk.WORD)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=text_widget.yview)
    
    text_widget.insert(tk.END, data_text)
    text_widget.config(state=tk.DISABLED)


def show_statistics(user):
    if not user.strip():
        messagebox.showwarning("Warning", "Please enter a user name first!")
        return
    
    try:
        conn = sqlite3.connect(data_file)
        df = pd.read_sql_query(
            "SELECT * FROM bmi_records WHERE user = ? ORDER BY date, created_at", 
            conn, params=[user]
        )
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Database error: {str(e)}")
        return
    except Exception as e:
        messagebox.showerror("Error", f"No data found: {str(e)}")
        return

    if df.empty:
        messagebox.showinfo("Info", f"No BMI data found for user '{user}'.")
        return

    bmis = df['bmi'].tolist()
    categories = df['category'].tolist()
    
    # Calculate statistics
    avg_bmi = sum(bmis) / len(bmis)
    min_bmi = min(bmis)
    max_bmi = max(bmis)
    latest_bmi = bmis[-1]
    
    # Category counts
    category_counts = {}
    for cat in categories:
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    # BMI trend
    if len(bmis) > 1:
        trend = "📈 Increasing" if bmis[-1] > bmis[0] else "📉 Decreasing" if bmis[-1] < bmis[0] else "➡️ Stable"
    else:
        trend = "➡️ Insufficient data for trend"
    
    stats_message = f"""📊 BMI Statistics for {user}
    
📈 Summary:
• Total Records: {len(bmis)}
• Average BMI: {avg_bmi:.2f}
• Current BMI: {latest_bmi:.2f}
• Minimum BMI: {min_bmi:.2f}
• Maximum BMI: {max_bmi:.2f}
• Overall Trend: {trend}

📋 Category Distribution:"""
    
    for category, count in category_counts.items():
        percentage = (count / len(bmis)) * 100
        stats_message += f"\n• {category}: {count} records ({percentage:.1f}%)"
    
    messagebox.showinfo("BMI Statistics", stats_message)


def plot_user_bmi(user):
    if not user.strip():
        messagebox.showwarning("Warning", "Please enter a user name first!")
        return
    
    try:
        conn = sqlite3.connect(data_file)
        df = pd.read_sql_query(
            "SELECT * FROM bmi_records WHERE user = ? ORDER BY date, created_at", 
            conn, params=[user]
        )
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Database error: {str(e)}")
        return
    except Exception as e:
        messagebox.showerror("Error", f"No data found: {str(e)}")
        return

    if df.empty:
        messagebox.showinfo("Info", f"No BMI data found for user '{user}'.")
        return

    dates = df['date'].tolist()
    bmis = df['bmi'].tolist()
    categories = df['category'].tolist()

    # Create figure with larger size
    plt.figure(figsize=(12, 8))
    
    # Color code points based on BMI category
    colors = []
    for category in categories:
        if category == "Underweight":
            colors.append("#3498db")
        elif category == "Normal":
            colors.append("#27ae60")
        elif category == "Overweight":
            colors.append("#f39c12")
        else:  # Obese
            colors.append("#e74c3c")
    
    # Plot with colored markers
    plt.scatter(dates, bmis, c=colors, s=100, alpha=0.7, edgecolors='black', linewidth=1)
    plt.plot(dates, bmis, 'k--', alpha=0.5, linewidth=1)
    
    # Add BMI category lines
    plt.axhline(y=18.5, color='#3498db', linestyle=':', alpha=0.7, label='Underweight')
    plt.axhline(y=24.9, color='#27ae60', linestyle=':', alpha=0.7, label='Normal')
    plt.axhline(y=29.9, color='#f39c12', linestyle=':', alpha=0.7, label='Overweight')
    
    plt.title(f"📊 {user}'s BMI Trend Analysis", fontsize=16, fontweight='bold')
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("BMI Value", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Add statistics text box
    avg_bmi = sum(bmis) / len(bmis)
    latest_bmi = bmis[-1]
    min_bmi = min(bmis)
    max_bmi = max(bmis)
    
    stats_text = f'📈 Statistics:\nAverage BMI: {avg_bmi:.2f}\nLatest BMI: {latest_bmi:.2f}\nMin BMI: {min_bmi:.2f}\nMax BMI: {max_bmi:.2f}\nTotal Records: {len(bmis)}'
    plt.text(0.02, 0.98, stats_text, transform=plt.gca().transAxes, 
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
             verticalalignment='top', fontsize=10)
    
    plt.tight_layout()
    plt.show()


def on_calculate():
    user = user_entry.get()
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        bmi = calculate_bmi(weight, height)
        category = get_category(bmi)
        # Color code based on category
        if category == "Underweight":
            color = "#3498db"
        elif category == "Normal":
            color = "#27ae60"
        elif category == "Overweight":
            color = "#f39c12"
        else:  # Obese
            color = "#e74c3c"

        result_label.config(text=f"📊 BMI: {bmi:.2f} ({category})", fg=color)
        bmi_record = {
            "date": str(datetime.now().date()),
            "weight": weight,
            "height": height,
            "bmi": round(bmi, 2),
            "category": category
        }
        save_data(user, bmi_record)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")


# GUI Setup
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("400x500")
root.configure(bg="#2c3e50")
root.resizable(False, False)

# Configure style
header_font = ("Arial", 18, "bold")
label_font = ("Arial", 11, "bold")
entry_font = ("Arial", 10)
button_font = ("Arial", 12, "bold")
result_font = ("Arial", 14, "bold")

# Header
header = tk.Label(root,
                  text="💪 BMI Calculator",
                  font=header_font,
                  bg="#2c3e50",
                  fg="#ecf0f1")
header.grid(row=0, column=0, columnspan=2, pady=(20, 30))

# User Name
user_label = tk.Label(root,
                      text="👤 User Name:",
                      font=label_font,
                      bg="#2c3e50",
                      fg="#ecf0f1")
user_label.grid(row=1, column=0, sticky="e", padx=(20, 10), pady=10)
user_entry = tk.Entry(root,
                      font=entry_font,
                      width=20,
                      relief="flat",
                      bd=5,
                      bg="#ecf0f1",
                      fg="#2c3e50")
user_entry.grid(row=1, column=1, padx=(0, 20), pady=10)

# Weight
weight_label = tk.Label(root,
                        text="⚖️ Weight (kg):",
                        font=label_font,
                        bg="#2c3e50",
                        fg="#ecf0f1")
weight_label.grid(row=2, column=0, sticky="e", padx=(20, 10), pady=10)
weight_entry = tk.Entry(root,
                        font=entry_font,
                        width=20,
                        relief="flat",
                        bd=5,
                        bg="#ecf0f1",
                        fg="#2c3e50")
weight_entry.grid(row=2, column=1, padx=(0, 20), pady=10)

# Height
height_label = tk.Label(root,
                        text="📏 Height (m):",
                        font=label_font,
                        bg="#2c3e50",
                        fg="#ecf0f1")
height_label.grid(row=3, column=0, sticky="e", padx=(20, 10), pady=10)
height_entry = tk.Entry(root,
                        font=entry_font,
                        width=20,
                        relief="flat",
                        bd=5,
                        bg="#ecf0f1",
                        fg="#2c3e50")
height_entry.grid(row=3, column=1, padx=(0, 20), pady=10)

# Calculate Button
calculate_btn = tk.Button(root,
                          text="🧮 Calculate BMI",
                          command=on_calculate,
                          font=button_font,
                          bg="#3498db",
                          fg="white",
                          relief="flat",
                          bd=0,
                          pady=10,
                          cursor="hand2",
                          activebackground="#2980b9",
                          activeforeground="white")
calculate_btn.grid(row=4,
                   column=0,
                   columnspan=2,
                   pady=20,
                   padx=20,
                   sticky="ew")

# Result
result_label = tk.Label(root,
                        text="",
                        font=result_font,
                        bg="#2c3e50",
                        fg="#e74c3c",
                        wraplength=350)
result_label.grid(row=5, column=0, columnspan=2, pady=(0, 20))

# Buttons frame for better layout
button_frame = tk.Frame(root, bg="#2c3e50")
button_frame.grid(row=6, column=0, columnspan=2, pady=(0, 10), padx=20, sticky="ew")
button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)

# Plot Button
plot_btn = tk.Button(button_frame,
                     text="📊 View BMI History",
                     command=lambda: plot_user_bmi(user_entry.get()),
                     font=button_font,
                     bg="#27ae60",
                     fg="white",
                     relief="flat",
                     bd=0,
                     pady=8,
                     cursor="hand2",
                     activebackground="#229954",
                     activeforeground="white")
plot_btn.grid(row=0, column=0, padx=(0, 5), sticky="ew")

# Statistics Button
stats_btn = tk.Button(button_frame,
                      text="📈 View Statistics",
                      command=lambda: show_statistics(user_entry.get()),
                      font=button_font,
                      bg="#9b59b6",
                      fg="white",
                      relief="flat",
                      bd=0,
                      pady=8,
                      cursor="hand2",
                      activebackground="#8e44ad",
                      activeforeground="white")
stats_btn.grid(row=0, column=1, padx=(5, 0), sticky="ew")

# View Database Button
view_db_btn = tk.Button(root,
                        text="🗃️ View Database",
                        command=view_all_data,
                        font=button_font,
                        bg="#34495e",
                        fg="white",
                        relief="flat",
                        bd=0,
                        pady=8,
                        cursor="hand2",
                        activebackground="#2c3e50",
                        activeforeground="white")
view_db_btn.grid(row=7, column=0, columnspan=2, pady=(0, 20), padx=20, sticky="ew")

root.mainloop()
