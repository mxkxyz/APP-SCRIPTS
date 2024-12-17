import pyttsx3
import PyPDF2
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from tkinter.ttk import Combobox, Progressbar
from threading import Thread, Lock

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine_lock = Lock()
paused = False
text_to_read = ""
engine_thread = None

def text_to_speech(text, voice='female', rate_adjustment=0):
    global paused, engine_thread
    paused = False
    voices = engine.getProperty('voices')
    for voice_option in voices:
        if voice in voice_option.name.lower():
            engine.setProperty('voice', voice_option.id)
            break

    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate + rate_adjustment)

    def run_engine():
        with engine_lock:
            engine.say(text)
            engine.runAndWait()

    engine_thread = Thread(target=run_engine)
    engine_thread.start()

def pause_speech():
    global paused
    with engine_lock:
        engine.stop()
    paused = True

def resume_speech():
    global paused, text_to_read
    if paused:
        text_to_speech(text_to_read, voice_var.get(), int(rate_var.get()))
    paused = False

def read_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                text += page.extractText()
        return text
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read PDF: {e}")
        return ""

def on_read():
    global text_to_read
    text = text_area.get("1.0", tk.END).strip()
    if text:
        text_to_read = text
        text_to_speech(text, voice_var.get(), int(rate_var.get()))
    else:
        messagebox.showwarning("Warning", "Please enter text to read.")
    update_progress_bar()

def on_pause():
    pause_speech()
    update_progress_bar(pause=True)

def on_resume():
    resume_speech()
    update_progress_bar()

def on_open_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        pdf_text = read_pdf(file_path)
        if pdf_text:
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, pdf_text)

def update_progress_bar(pause=False):
    if pause:
        progress_bar.stop()
        progress_bar['value'] = 50
    else:
        progress_bar.start()

# Create the main window
window = tk.Tk()
window.title("Readme TTS")
window.geometry("800x700")

# Apply a custom color theme
bg_color = "#282c34"
fg_color = "#abb2bf"
highlight_color = "#61afef"
button_color = "#98c379"

window.configure(bg=bg_color)

# Create a transparent watermark with "M Y K X Y Z"
canvas = tk.Canvas(window, width=800, height=700, bg=bg_color, highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_text(400, 350, text="M Y K X Y Z-T X T-R E A D E R", font=("Helvetica", 37, "bold"), fill="#555555", angle=0, tags="watermark")

# Bring other widgets to the front
def raise_above_watermark(widget):
    window.after(0, widget.tkraise)

# Create a label for the app name
app_name_label = tk.Label(window, text="Enter text to be Read below", font=("Helvetica", 24, "bold"), fg=highlight_color, bg=bg_color)
app_name_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
raise_above_watermark(app_name_label)

# Create a text area for input
text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=10, fg=fg_color, bg=bg_color, insertbackground=fg_color, highlightbackground=highlight_color)
text_area.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
raise_above_watermark(text_area)

# Create buttons
read_button = tk.Button(window, text="Read", command=on_read, fg=bg_color, bg=button_color)
read_button.place(relx=0.2, rely=0.45, anchor=tk.CENTER)
raise_above_watermark(read_button)

pause_button = tk.Button(window, text="Pause", command=on_pause, fg=bg_color, bg=button_color)
pause_button.place(relx=0.4, rely=0.45, anchor=tk.CENTER)
raise_above_watermark(pause_button)

resume_button = tk.Button(window, text="Resume", command=on_resume, fg=bg_color, bg=button_color)
resume_button.place(relx=0.6, rely=0.45, anchor=tk.CENTER)
raise_above_watermark(resume_button)

open_pdf_button = tk.Button(window, text="Open PDF", command=on_open_pdf, fg=bg_color, bg=button_color)
open_pdf_button.place(relx=0.8, rely=0.45, anchor=tk.CENTER)
raise_above_watermark(open_pdf_button)

# Add TTS settings
settings_frame = tk.Frame(window, bg=bg_color)
settings_frame.place(relx=0.5, rely=0.55, anchor=tk.CENTER)
raise_above_watermark(settings_frame)

tk.Label(settings_frame, text="Voice:", fg=fg_color, bg=bg_color).pack(side=tk.LEFT, padx=5)
voice_var = tk.StringVar(value='female')
voice_options = [voice.name for voice in engine.getProperty('voices') if 'female' in voice.name.lower() or 'male' in voice.name.lower()]
voice_dropdown = Combobox(settings_frame, textvariable=voice_var, values=voice_options, state="readonly")
voice_dropdown.pack(side=tk.LEFT, padx=5)

tk.Label(settings_frame, text="Speed:", fg=fg_color, bg=bg_color).pack(side=tk.LEFT, padx=5)
rate_var = tk.StringVar(value='0')
rate_dropdown = Combobox(settings_frame, textvariable=rate_var, values=[str(i) for i in range(-100, 101, 10)], state="readonly")
rate_dropdown.pack(side=tk.LEFT, padx=5)

# Create a progress bar
progress_bar = Progressbar(window, orient='horizontal', mode='indeterminate', length=400)
progress_bar.place(relx=0.5, rely=0.65, anchor=tk.CENTER)
raise_above_watermark(progress_bar)

# Start the Tkinter event loop
paused = False
window.mainloop()

## Copyright 2024 MYKXYZ Inc. All rights reserved.