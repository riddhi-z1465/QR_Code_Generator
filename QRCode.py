import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import qrcode
from PIL import Image, ImageTk
import os
from tkinterdnd2 import DND_FILES, TkinterDnD

# Function to generate QR code
def generate_qr():
    text = entry.get()
    if not text:
        messagebox.showerror("Error", "Please enter text or URL")
        return

    # Generate QR code
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(text)
    qr.make(fit=True)

    # Apply selected color theme
    theme = theme_var.get()
    if theme == "Cyber Theme":
        fg_color, bg_color = "#00FFFF", "#000000"
    else:
        fg_color, bg_color = "#FF69B4", "#FFFFFF"

    img = qr.make_image(fill_color=fg_color, back_color=bg_color)
    img = img.resize((200, 200))  # Resize for UI display

    # Save QR temporarily for preview
    temp_path = "temp_qr.png"
    img.save(temp_path)
    show_qr_animation(temp_path)

# Function to display QR
def show_qr_animation(img_path):
    img = Image.open(img_path)
    img = ImageTk.PhotoImage(img)
    qr_label.config(image=img)
    qr_label.image = img

# Function to save QR code
def save_qr():
    temp_path = "temp_qr.png"

    if not os.path.exists(temp_path):
        messagebox.showerror("Error", "No QR code generated to save!")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        os.rename(temp_path, file_path)
        messagebox.showinfo("Success", "QR Code saved successfully!")

# Function to handle drag-and-drop
def on_drop(event):
    dropped_text = event.data.strip("{}")
    entry.delete(0, tk.END)
    entry.insert(0, dropped_text)

# Function to apply hover effects on buttons
def on_enter(e):
    e.widget.config(style="Hover.TButton")

def on_leave(e):
    e.widget.config(style="TButton")

# GUI Setup
root = TkinterDnD.Tk()
root.title("QR Code Generator")
root.geometry("420x600")
root.configure(bg="#222831")  # Dark background

# Styling
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=6, background="#393E46", foreground="white")
style.configure("Hover.TButton", font=("Arial", 12, "bold"), padding=6, background="#00ADB5", foreground="white")

# Title Label
tk.Label(root, text="QR Code Generator", fg="#00ADB5", bg="#222831", font=("Arial", 20, "bold")).pack(pady=10)

#label for entering text or URl
tk.Label(root, text="Enter Text or URL:", fg="white", bg="#1e1e1e", font=("Arial", 12)).pack(pady=5)

# Entry Field
entry = tk.Entry(root, width=45, font=("Arial", 12))
entry.pack(pady=10)
entry.drop_target_register(DND_FILES)
entry.dnd_bind('<<Drop>>', on_drop)

# Theme selection menu
theme_var = tk.StringVar(value="Cyber Theme")
theme_menu = ttk.OptionMenu(root, theme_var, "Cyber Theme", "Minimal White")
theme_menu.pack(pady=5)

# Generate QR Button
generate_btn = ttk.Button(root, text="Generate QR", command=generate_qr)
generate_btn.pack(pady=5)
generate_btn.bind("<Enter>", on_enter)
generate_btn.bind("<Leave>", on_leave)

# Save Button
save_btn = ttk.Button(root, text="Save QR", command=save_qr)
save_btn.pack(pady=5)
save_btn.bind("<Enter>", on_enter)
save_btn.bind("<Leave>", on_leave)

# QR Code Display (Now placed after Save button)
qr_label = tk.Label(root, bg="#222831")
qr_label.pack(pady=20)  # Increased padding to create space below Save button

root.mainloop()
