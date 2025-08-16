import tkinter as tk
from tkinter import font
from pynput.mouse import Controller, Button, Listener
from pynput import keyboard
import threading
import time

mouse = Controller()
clicking = False
click_position = None

# --- Auto Clicker Functions ---

def record_position():
    """Wait for the user to click somewhere to record position"""
    global recording
    recording = True
    status_label.config(text="Click anywhere to set position...", fg="black")

    def on_click(x, y, button, pressed):
        global click_position, recording
        if pressed and recording:
            click_position = (x, y)
            coords_label.config(text=f"Recorded: {click_position}")
            status_label.config(text="Status: Position recorded", fg="black")
            recording = False
            return False  # stop listener after one click

    listener = Listener(on_click=on_click)
    listener.start()

def click_loop():
    """Background clicking loop"""
    global clicking
    while clicking:
        if click_position:
            mouse.position = click_position
            mouse.click(Button.left, 1)
        time.sleep(0.01)  # adjust click speed

def start_clicking():
    """Start clicking in a new thread"""
    global clicking
    if click_position:
        clicking = True
        threading.Thread(target=click_loop, daemon=True).start()
        status_label.config(text="Status: Clicking", fg="black")
    else:
        status_label.config(text="No position recorded!", font="", fg="red")

def stop_clicking():
    """Stop clicking"""
    global clicking
    clicking = False
    status_label.config(text="Status: Stopped", fg="red")

def toggle_clicking():
    """Toggle between start/stop"""
    global clicking
    if clicking:
        stop_clicking()
    else:
        start_clicking()

# --- Keyboard Hotkey Listener (F6 to stop) ---

def on_press(key):
    global clicking
    try:
        if key == keyboard.Key.f6:  # Force Stop
            stop_clicking()
        elif key == keyboard.Key.f7:  # Start/Stop Toggle
            toggle_clicking()
        elif key == keyboard.Key.f8:  # Record Mouse Position
            record_position()
    except AttributeError:
        pass

listener = keyboard.Listener(on_press=on_press)
listener.start()

#def open_options():
#    return

# --- GUI Setup ---

root = tk.Tk()
root.title("Auto Clicker")
root.geometry("240x200")

#menubar = tk.Menu(root)
#options_menu = tk.Menu(menubar, tearoff=0)
#options_menu.add_command(label="Hotkeys", command=open_options)
#menubar.add_cascade(label="Options", menu=options_menu)
#root.config(menu=menubar)

coords_label = tk.Label(root, text="No position recorded")
coords_label.pack(pady=8)

record_btn = tk.Button(root, text="Record Position (F8)", command=record_position)
record_btn.pack(pady=10)

start_btn = tk.Button(root, text="Toggle Clicking (F7)", command=start_clicking)
start_btn.pack(pady=10)

#stop_btn = tk.Button(root, text="Stop Clicking (F7)", command=stop_clicking)
#stop_btn.pack(pady=9)

status_label = tk.Label(root, text="Status: Stopped")
status_label.pack(pady=8)

footer_label = tk.Label(root, text="Made with love... and Chat GPT.", font=("ComicSans", 8, "italic"), fg="#555555", anchor="center")
footer_label.pack(side="bottom", pady=2)

root.mainloop()
