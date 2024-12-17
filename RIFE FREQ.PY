import tkinter as tk
from tkinter import ttk
import pygame
import numpy as np
import traceback

# Initialize pygame mixer with stereo settings
pygame.mixer.init(frequency=44100, size=-16, channels=2)

# Rife frequency list with descriptions
frequencies = {
    "728 Hz": "General antiseptic effect.",
    "784 Hz": "Tuberculosis, General use, Arthritis.",
    "880 Hz": "Cold, Infections.",
    # Add more frequencies and descriptions here
}

def generate_sine_wave(frequency, duration=10, sample_rate=44100):
    try:
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        sine_wave = 0.5 * np.sin(2 * np.pi * frequency * t)
        stereo_wave = np.column_stack((sine_wave, sine_wave))
        if stereo_wave.ndim != 2 or stereo_wave.shape[1] != 2:
            raise ValueError(f"Stereo wave shape incorrect: {stereo_wave.shape}")
        return stereo_wave
    except Exception as e:
        log_error(f"Error in generate_sine_wave: {e}\n{traceback.format_exc()}")
        raise

def play_frequency(frequency):
    try:
        sine_wave = generate_sine_wave(frequency)
        audio_data = np.int16(sine_wave * 32767)
        log_error(f"Generated audio data shape: {audio_data.shape}")
        sound = pygame.sndarray.make_sound(audio_data)
        sound.play()
    except Exception as e:
        log_error(f"Error in play_frequency: {e}\n{traceback.format_exc()}")
        raise

def on_play_button_click():
    try:
        selected_freq = frequency_combo.get()
        if selected_freq:
            frequency = int(selected_freq.split()[0])
            play_frequency(frequency)
    except Exception as e:
        log_error(f"Error in on_play_button_click: {e}\n{traceback.format_exc()}")
        raise

def update_description(event):
    try:
        selected_freq = frequency_combo.get()
        description = frequencies.get(selected_freq, "")
        description_label.config(text=description)
    except Exception as e:
        log_error(f"Error in update_description: {e}\n{traceback.format_exc()}")
        raise

def log_error(message):
    error_text.insert(tk.END, message + "\n")
    error_text.see(tk.END)

# Create the main window
root = tk.Tk()
root.title("Rife Frequency Player")

# Create and place the frequency dropdown
frequency_label = ttk.Label(root, text="Select Frequency:")
frequency_label.pack(pady=5)

frequency_combo = ttk.Combobox(root, values=list(frequencies.keys()))
frequency_combo.pack(pady=5)

# Create and place the description label
description_label = ttk.Label(root, text="", wraplength=300)
description_label.pack(pady=5)

frequency_combo.bind("<<ComboboxSelected>>", update_description)

# Create and place the play button
play_button = ttk.Button(root, text="Play Frequency", command=on_play_button_click)
play_button.pack(pady=10)

import tkinter as tk
from tkinter import ttk
import pygame
import numpy as np
import traceback

# Initialize pygame mixer with stereo settings
pygame.mixer.init(frequency=44100, size=-16, channels=2)

# Rife frequency list with descriptions
frequencies = {
    "728 Hz": "General antiseptic effect.",
    "784 Hz": "Tuberculosis, General use, Arthritis.",
    "880 Hz": "Cold, Infections.",
    # Add more frequencies and descriptions here
}

def generate_sine_wave(frequency, duration=10, sample_rate=44100):
    try:
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        sine_wave = 0.5 * np.sin(2 * np.pi * frequency * t)
        stereo_wave = np.column_stack((sine_wave, sine_wave))
        if stereo_wave.ndim != 2 or stereo_wave.shape[1] != 2:
            raise ValueError(f"Stereo wave shape incorrect: {stereo_wave.shape}")
        return stereo_wave
    except Exception as e:
        log_error(f"Error in generate_sine_wave: {e}\n{traceback.format_exc()}")
        raise

def play_frequency(frequency):
    try:
        sine_wave = generate_sine_wave(frequency)
        audio_data = np.int16(sine_wave * 32767)
        log_error(f"Generated audio data shape: {audio_data.shape}")
        sound = pygame.sndarray.make_sound(audio_data)
        sound.play()
    except Exception as e:
        log_error(f"Error in play_frequency: {e}\n{traceback.format_exc()}")
        raise

def on_play_button_click():
    try:
        selected_freq = frequency_combo.get()
        if selected_freq:
            frequency = int(selected_freq.split()[0])
            play_frequency(frequency)
    except Exception as e:
        log_error(f"Error in on_play_button_click: {e}\n{traceback.format_exc()}")
        raise

def update_description(event):
    try:
        selected_freq = frequency_combo.get()
        description = frequencies.get(selected_freq, "")
        description_label.config(text=description)
    except Exception as e:
        log_error(f"Error in update_description: {e}\n{traceback.format_exc()}")
        raise

def log_error(message):
    error_text.insert(tk.END, message + "\n")
    error_text.see(tk.END)

# Create the main window
root = tk.Tk()
root.title("Rife Frequency Player")

# Create and place the frequency dropdown
frequency_label = ttk.Label(root, text="Select Frequency:")
frequency_label.pack(pady=5)

frequency_combo = ttk.Combobox(root, values=list(frequencies.keys()))
frequency_combo.pack(pady=5)

# Create and place the description label
description_label = ttk.Label(root, text="", wraplength=300)
description_label.pack(pady=5)

frequency_combo.bind("<<ComboboxSelected>>", update_description)

# Create and place the play button
play_button = ttk.Button(root, text="Play Frequency", command=on_play_button_click)
play_button.pack(pady=5)

# Create and place the continuous play button with toggle
continuous_play_var = tk.BooleanVar()
continuous_play_button = ttk.Checkbutton(root, text="Continuous Play", variable=continuous_play_var, command=on_continuous_play_button_click)
continuous_play_button.pack(pady=5)

# Create and place the stop button
stop_button = ttk.Button(root, text="Stop Playback", command=stop_playback)
stop_button.pack(pady=5)

# Create and place the frequency slider
frequency_slider = tk.Scale(root, from_=0, to=1000, orient=tk.HORIZONTAL, label="Frequency (Hz)", command=update_frequency, background='black', foreground='green')
frequency_slider.pack(pady=10)

# Create and place the volume slider
volume_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Volume", background='black', foreground='green')
volume_slider.set(50)
volume_slider.pack(pady=5)

# Create and place the increment button
increment_button = ttk.Button(root, text="Increment Frequency", command=increment_frequency)
increment_button.pack(pady=5)

# Create and place the decrement button
decrement_button = ttk.Button(root, text="Decrement Frequency", command=decrement_frequency)
decrement_button.pack(pady=5)

# Create and place the error logging text area
error_text = tk.Text(root, height=10, wrap=tk.WORD, bg='black', fg='red')
error_text.pack(pady=10, fill=tk.BOTH, expand=True)

# Prepare the matplotlib figure
fig = plt.figure(facecolor='black')
ax = fig.add_subplot(111, projection='3d', facecolor='black')

# Generate grid coordinates for cymatics
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)

# Embed matplotlib figure in tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Animation for cymatic patterns
ani = FuncAnimation(fig, animate, frames=np.arange(0, 100), interval=100)

# RectangleSelector for pattern selection
selector = RectangleSelector(ax, on_select, drawtype='box', useblit=True, button=[1], minspanx=5, minspany=5, spancoords='pixels', interactive=True)

# Start the tkinter main loop
root.mainloop()

