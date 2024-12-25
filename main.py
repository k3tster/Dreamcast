import os
from datetime import datetime
from textblob import TextBlob
import csv
import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext

# Function to save a dream with the current date and sentiment
def save_dream(dream):
    date = datetime.now().strftime("%Y-%m-%d")
    sentiment = analyze_sentiment(dream)
    with open("data/dreams.txt", "a") as file:
        file.write(f"{date} | {sentiment} | {dream}\n")
    messagebox.showinfo("Success", "Your dream has been saved!")

# Function to analyze the sentiment of a dream
def analyze_sentiment(dream):
    blob = TextBlob(dream)
    sentiment = blob.sentiment.polarity  # Returns a float between -1 (negative) and +1 (positive)
    if sentiment > 0:
        return "Positive"
    elif sentiment < 0:
        return "Negative"
    else:
        return "Neutral"

# Function to view all saved dreams in the text box
def view_dreams():
    try:
        with open("data/dreams.txt", "r") as file:
            dreams = file.readlines()
            if dreams:
                dream_display.delete(1.0, tk.END)  # Clear existing text
                for dream in dreams:
                    dream_display.insert(tk.END, dream.strip() + "\n")
            else:
                messagebox.showinfo("Dream Journal", "No dreams saved yet.")
    except FileNotFoundError:
        messagebox.showinfo("Dream Journal", "No dreams saved yet.")

# Function to export dreams to CSV
def export_to_csv():
    try:
        with open("data/dreams.txt", "r") as file:
            dreams = file.readlines()
            with filedialog.asksaveasfile(mode='w', defaultextension=".csv") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["Date", "Sentiment", "Dream"])
                for dream in dreams:
                    parts = dream.strip().split(" | ")
                    if len(parts) == 3:
                        csv_writer.writerow(parts)
                messagebox.showinfo("Export", "Dreams exported successfully.")
    except FileNotFoundError:
        messagebox.showinfo("Export", "No dreams to export.")

# Main Tkinter application setup
root = tk.Tk()
root.title("DreamCast")
root.geometry("500x500")

# Dream entry section
tk.Label(root, text="Enter Your Dream:").pack(pady=10)
dream_entry = tk.Entry(root, width=60)
dream_entry.pack()

# Buttons for saving, analyzing, viewing, and exporting
tk.Button(root, text="Save Dream", command=lambda: save_dream(dream_entry.get())).pack(pady=5)

def analyze_and_save():
    dream = dream_entry.get()
    sentiment = analyze_sentiment(dream)
    messagebox.showinfo("Dream Analysis", f"The dream has a {sentiment} tone.")
    save_dream(dream)

tk.Button(root, text="Analyze and Save Tone", command=analyze_and_save).pack(pady=5)

tk.Button(root, text="View Dream Journal", command=view_dreams).pack(pady=5)
tk.Button(root, text="Export to CSV", command=export_to_csv).pack(pady=5)

# Scrollable text area for displaying dreams
dream_display = scrolledtext.ScrolledText(root, width=60, height=15)
dream_display.pack(pady=10)

# Run the Tkinter app
if not os.path.exists("data"):
    os.makedirs("data")
root.mainloop()

