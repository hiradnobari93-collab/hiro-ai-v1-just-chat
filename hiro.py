import tkinter as tk
from tkinter import scrolledtext, font
from ollama import Client
import threading
from datetime import datetime

print("hello im hiro ai (powered by hirad nobari)")

# --------- OLLAMA CONFIG ---------
OLLAMA_MODEL = "gpt-oss:120b-cloud"
OLLAMA_API_KEY = "b31cb30f4f894fd49749d76698d1b2da.o4YycMn5ctXMH5Y5vYRUiwUF"

def create_client(api_key):
    return Client(
        host="https://ollama.com",
        headers={"Authorization": f"Bearer {api_key}"}
    )

def ask_ollama(client, prompt):
    try:
        response = client.chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are Hiro AI. Answer briefly and to the point. Avoid unnecessary explanations."
                },
                {"role": "user", "content": prompt}
            ],
        )
        return response.message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Create client
client = create_client(OLLAMA_API_KEY)

# --------- GUI SETUP ---------
root = tk.Tk()
root.title("Hiro AI")
root.geometry("900x700")
root.configure(bg="#0a0e1a")

# Colors matching the HTML design
PRIMARY_ORANGE = "#ff6b35"
SECONDARY_ORANGE = "#ff8c42"
DARK_BG = "#0a0e1a"
CARD_BG = "#131829"
BORDER_COLOR = "#2a2a3e"
TEXT_PRIMARY = "#ffffff"
TEXT_SECONDARY = "#a0a0a0"

# Fonts
title_font = font.Font(family="Segoe UI", size=32, weight="normal")
status_font = font.Font(family="Segoe UI", size=10)
message_font = font.Font(family="Segoe UI", size=11)
input_font = font.Font(family="Segoe UI", size=12)
time_font = font.Font(family="Segoe UI", size=9)

# Header Frame
header_frame = tk.Frame(root, bg=DARK_BG)
header_frame.pack(pady=20, fill=tk.X)

# Status Bar
status_frame = tk.Frame(header_frame, bg="#1a1a2e", highlightbackground=BORDER_COLOR, highlightthickness=1)
status_frame.pack()

status_indicator = tk.Label(
    status_frame,
    text="●",
    fg=PRIMARY_ORANGE,
    bg="#1a1a2e",
    font=("Segoe UI", 8)
)
status_indicator.pack(side=tk.LEFT, padx=8, pady=5)

status_label = tk.Label(
    status_frame,
    text="Connected",
    fg=TEXT_SECONDARY,
    bg="#1a1a2e",
    font=status_font
)
status_label.pack(side=tk.LEFT, padx=8, pady=5)

# Logo and Title Frame
logo_title_frame = tk.Frame(header_frame, bg=DARK_BG)
logo_title_frame.pack(pady=20)

# Logo (using emoji as a simple replacement)
logo_label = tk.Label(
    logo_title_frame,
    text="⚡",
    fg="#ffffff",
    bg=PRIMARY_ORANGE,
    font=("Segoe UI", 32),
    width=2,
    height=1
)
logo_label.pack(side=tk.LEFT, padx=10)

# Title
title_label = tk.Label(
    logo_title_frame,
    text="Hiro AI",
    fg=TEXT_PRIMARY,
    bg=DARK_BG,
    font=title_font
)
title_label.pack(side=tk.LEFT, padx=10)

# Chat Container Frame
chat_container = tk.Frame(root, bg=CARD_BG, highlightbackground=BORDER_COLOR, highlightthickness=1)
chat_container.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

# Chat Display with Custom Scrollbar
chat_frame = tk.Frame(chat_container, bg=CARD_BG)
chat_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

# Canvas for messages
canvas = tk.Canvas(chat_frame, bg=CARD_BG, highlightthickness=0)
scrollbar = tk.Scrollbar(chat_frame, orient="vertical", command=canvas.yview, bg=CARD_BG, troughcolor=CARD_BG)
scrollable_frame = tk.Frame(canvas, bg=CARD_BG)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Input Frame
input_container = tk.Frame(root, bg=CARD_BG, highlightbackground=BORDER_COLOR, highlightthickness=1)
input_container.pack(padx=20, pady=10, fill=tk.X)

input_frame = tk.Frame(input_container, bg=CARD_BG)
input_frame.pack(fill=tk.X, padx=10, pady=10)

# Send Button (on the left)
send_btn = tk.Button(
    input_frame,
    text="➤",
    command=lambda: send_message(),
    font=("Segoe UI", 14, "bold"),
    bg=PRIMARY_ORANGE,
    fg="#ffffff",
    relief=tk.FLAT,
    width=3,
    height=1,
    cursor="hand2",
    activebackground=SECONDARY_ORANGE
)
send_btn.pack(side=tk.LEFT, padx=(0, 10))

# Input Entry
entry = tk.Text(
    input_frame,
    font=input_font,
    bg=CARD_BG,
    fg=TEXT_PRIMARY,
    insertbackground=TEXT_PRIMARY,
    relief=tk.FLAT,
    height=1,
    wrap=tk.WORD
)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

# Placeholder text
placeholder = "Ask me anything..."
entry.insert("1.0", placeholder)
entry.config(fg=TEXT_SECONDARY)

def on_entry_click(event):
    if entry.get("1.0", "end-1c") == placeholder:
        entry.delete("1.0", tk.END)
        entry.config(fg=TEXT_PRIMARY)

def on_focus_out(event):
    if entry.get("1.0", "end-1c").strip() == "":
        entry.insert("1.0", placeholder)
        entry.config(fg=TEXT_SECONDARY)

entry.bind("<FocusIn>", on_entry_click)
entry.bind("<FocusOut>", on_focus_out)

# Footer
footer_label = tk.Label(
    root,
    text="Powered by Hirad Nobari",
    fg=TEXT_SECONDARY,
    bg=DARK_BG,
    font=("Segoe UI", 9)
)
footer_label.pack(pady=10)

# Empty state
empty_state_label = tk.Label(
    scrollable_frame,
    text="💬\n\nStart a conversation with Hiro AI\nAsk me anything...",
    fg=TEXT_SECONDARY,
    bg=CARD_BG,
    font=("Segoe UI", 14),
    justify=tk.CENTER
)
empty_state_label.pack(pady=100)

def get_current_time():
    return datetime.now().strftime("%I:%M %p")

def add_message(text, is_user=True):
    # Remove empty state if exists
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    
    # Message Frame
    message_frame = tk.Frame(scrollable_frame, bg=CARD_BG)
    message_frame.pack(fill=tk.X, pady=10, padx=10)
    
    # Avatar
    avatar_bg = "#1e1e2e" if is_user else PRIMARY_ORANGE
    avatar_text = "👤" if is_user else "⚡"
    
    avatar = tk.Label(
        message_frame,
        text=avatar_text,
        bg=avatar_bg,
        fg="#ffffff",
        font=("Segoe UI", 16),
        width=2,
        height=1
    )
    avatar.pack(side=tk.LEFT, anchor="n", padx=(0, 10))
    
    # Message Content Frame
    content_frame = tk.Frame(message_frame, bg=CARD_BG)
    content_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    # Header (Name + Time)
    header_frame = tk.Frame(content_frame, bg=CARD_BG)
    header_frame.pack(anchor="w")
    
    name_label = tk.Label(
        header_frame,
        text="You" if is_user else "Hiro AI",
        fg=TEXT_PRIMARY,
        bg=CARD_BG,
        font=("Segoe UI", 10, "bold")
    )
    name_label.pack(side=tk.LEFT, padx=(0, 10))
    
    time_label = tk.Label(
        header_frame,
        text=get_current_time(),
        fg=TEXT_SECONDARY,
        bg=CARD_BG,
        font=time_font
    )
    time_label.pack(side=tk.LEFT)
    
    # Message Text
    msg_bg = "#2a1f1a" if is_user else "#1a1a2e"
    msg_border = "#4a3020" if is_user else "#2a2a3e"
    
    message_text = tk.Label(
        content_frame,
        text=text,
        fg=TEXT_PRIMARY,
        bg=msg_bg,
        font=message_font,
        justify=tk.LEFT,
        wraplength=600,
        anchor="w",
        padx=20,
        pady=12
    )
    message_text.pack(anchor="w", pady=(5, 0), fill=tk.X)
    
    # Scroll to bottom
    canvas.update_idletasks()
    canvas.yview_moveto(1.0)

def show_typing_indicator():
    typing_frame = tk.Frame(scrollable_frame, bg=CARD_BG, name="typing_indicator")
    typing_frame.pack(fill=tk.X, pady=10, padx=10)
    
    avatar = tk.Label(
        typing_frame,
        text="⚡",
        bg=PRIMARY_ORANGE,
        fg="#ffffff",
        font=("Segoe UI", 16),
        width=2,
        height=1
    )
    avatar.pack(side=tk.LEFT, anchor="n", padx=(0, 10))
    
    typing_label = tk.Label(
        typing_frame,
        text="●  ●  ●",
        fg=PRIMARY_ORANGE,
        bg=CARD_BG,
        font=("Segoe UI", 14)
    )
    typing_label.pack(side=tk.LEFT)
    
    canvas.update_idletasks()
    canvas.yview_moveto(1.0)

def remove_typing_indicator():
    for widget in scrollable_frame.winfo_children():
        if str(widget) == ".!frame.!frame2.!frame.!canvas.!frame.typing_indicator":
            widget.destroy()

def send_message():
    message = entry.get("1.0", "end-1c").strip()
    
    if not message or message == placeholder:
        return
    
    # Disable send button
    send_btn.config(state=tk.DISABLED)
    
    # Add user message
    add_message(message, is_user=True)
    
    # Clear entry
    entry.delete("1.0", tk.END)
    
    # Show typing indicator
    show_typing_indicator()
    
    # Get AI response in a separate thread
    def get_response():
        response = ask_ollama(client, message)
        root.after(0, lambda: display_response(response))
    
    threading.Thread(target=get_response, daemon=True).start()

def display_response(response):
    remove_typing_indicator()
    add_message(response, is_user=False)
    send_btn.config(state=tk.NORMAL)

# Bind Enter key
def on_enter(event):
    if event.state & 0x1:  # Shift is pressed
        return
    else:
        send_message()
        return "break"

entry.bind("<Return>", on_enter)

# Auto-resize entry
def on_entry_change(event):
    lines = entry.get("1.0", "end-1c").count('\n') + 1
    if lines > 5:
        lines = 5
    entry.config(height=lines)

entry.bind("<KeyRelease>", on_entry_change)

# Animate status indicator
def animate_status():
    current_color = status_indicator.cget("fg")
    if current_color == PRIMARY_ORANGE:
        status_indicator.config(fg="#ff8c42")
    else:
        status_indicator.config(fg=PRIMARY_ORANGE)
    root.after(1000, animate_status)

animate_status()

# Start GUI
root.mainloop()