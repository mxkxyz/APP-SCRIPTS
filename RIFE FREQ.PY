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

# Create a
