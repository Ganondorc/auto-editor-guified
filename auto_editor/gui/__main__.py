import tkinter as tk
from tkinter import filedialog, messagebox
from auto_editor import edit_media  # Assuming this function can be imported and used directly

def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.mkv"), ("All files", "*.*")])
    if filepath:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, filepath)

def start_editing():
    input_file = file_entry.get()
    silent_speed = silent_speed_var.get()
    # Add other parameters handling here

    try:
        # Assuming edit_media can directly use these parameters
        edit_media(input_file, silent_speed=silent_speed)
        messagebox.showinfo("Success", "Video editing is complete")
    except Exception as e:
        messagebox.showerror("Error", str(e))

app = tk.Tk()
app.title("Auto-Editor GUI")

file_entry = tk.Entry(app, width=50)
file_entry.pack(pady=20)

open_button = tk.Button(app, text="Open File", command=open_file)
open_button.pack(pady=5)

silent_speed_var = tk.StringVar()
silent_speed_entry = tk.Entry(app, textvariable=silent_speed_var)
silent_speed_entry.pack(pady=10)

start_button = tk.Button(app, text="Start Editing", command=start_editing)
start_button.pack(pady=20)

app.mainloop()
