import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import RectangleSelector
from matplotlib.animation import FuncAnimation
import pygame
import traceback
import threading

# Initialize pygame mixer with stereo settings
pygame.mixer.init(frequency=44100, size=-16, channels=2)

# Rife frequency list with descriptions
frequencies = {
    "160 Hz": "Carrier frequency paired with a binaural beat frequency of 0.5 Hz for headache relief.",
    "4-8 Hz": "Theta brain wave frequency associated with meditation and relaxation.",
    "728 Hz": "General antiseptic effect.",
    "784 Hz": "Tuberculosis, General use, Arthritis.",
    "880 Hz": "Cold, Infections.",
    "528 Hz": "DNA repair, Cell regeneration.",
    "432 Hz": "Healing, Harmonic resonance.",
    "174 Hz": "Pain relief, Anaesthetic properties.",
    "396 Hz": "Liberating guilt and fear.",
    "285 Hz": "Healing of cuts, burns, and wounds.",
    "963 Hz": "Awakening intuition, Crown chakra.",
    "852 Hz": "Returning to spiritual order.",
    "639 Hz": "Enhancing relationships, Connection.",
    "741 Hz": "Detoxification, Solving problems.",
    "417 Hz": "Facilitating change, Cleansing traumatic experiences.",
    "369 Hz": "Healing frequencies, Cleanses cells.",
}

def generate_sine_wave(frequency, duration=10, sample_rate=44100):
    try:
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        sine_wave = 0.5 * np.sin(2 * np.pi * frequency * t)
        stereo_wave = np.column_stack((sine_wave, sine_wave))  # Ensure stereo format
        return stereo_wave
    except Exception as e:
        log_error(f"Error in generate_sine_wave: {e}\n{traceback.format_exc()}")
        raise

def play_frequency(frequency, volume=1.0):
    try:
        stereo_wave = generate_sine_wave(frequency)
        audio_data = np.int16(stereo_wave * 32767 * volume)
        if audio_data.ndim != 2 or audio_data.shape[1] != 2:
            raise ValueError("Audio data must be stereo (2 channels).")
        sound = pygame.sndarray.make_sound(audio_data)
        sound.play()
    except Exception as e:
        log_error(f"Error in play_frequency: {e}\n{traceback.format_exc()}")
        raise

def stop_playback():
    try:
        pygame.mixer.stop()
    except Exception as e:
        log_error(f"Error in stop_playback: {e}\n{traceback.format_exc()}")
        raise

def update_frequency(val):
    try:
        frequency = float(val)
        frequency_label.config(text=f"Frequency: {frequency} Hz")
        update_cymatic_pattern(frequency)
        play_frequency(frequency, volume_slider.get() / 100.0)
    except Exception as e:
        log_error(f"Error in update_frequency: {e}\n{traceback.format_exc()}")
        raise

def on_play_button_click():
    try:
        selected_freq = frequency_combo.get()
        if selected_freq:
            if selected_freq == "4-8 Hz":
                # Play a combination of frequencies from 4 to 8 Hz
                for freq in range(4, 9):
                    play_frequency(freq, volume_slider.get() / 100.0)
            else:
                frequency = float(selected_freq.split()[0])
                play_frequency(frequency, volume_slider.get() / 100.0)
                update_cymatic_pattern(frequency)
    except Exception as e:
        log_error(f"Error in on_play_button_click: {e}\n{traceback.format_exc()}")
        raise

def on_continuous_play_button_click():
    try:
        stop_playback()  # Stop any ongoing playback
        selected_freq = frequency_combo.get()
        if selected_freq:
            frequency = float(selected_freq.split()[0])
            while continuous_play_var.get():
                play_frequency(frequency, volume_slider.get() / 100.0)
    except Exception as e:
        log_error(f"Error in on_continuous_play_button_click: {e}\n{traceback.format_exc()}")
        raise

def update_description(event):
    try:
        selected_freq = frequency_combo.get()
        description = frequencies.get(selected_freq, "")
        description_label.config(text=description)
    except Exception as e:
        log_error(f"Error in update_description: {e}\n{traceback.format_exc()}")
        raise

def update_cymatic_pattern(frequency):
    try:
        pattern = cymatics_pattern(frequency)
        ax.clear()
        ax.plot_surface(X, Y, pattern, cmap='viridis')
        ax.set_title(f'Cymatic Pattern at {frequency} Hz')
        ax.set_facecolor('black')
        ax.set_xticks([])  # Hide the x-axis
        ax.set_yticks([])  # Hide the y-axis
        ax.set_zticks([])  # Hide the z-axis
        # Centering the logo
        ax.text2D(0.5, 0.95, "SOUNDFR3QK", transform=ax.transAxes, fontsize=24, color='orange', alpha=0.5, ha='center')
        canvas.draw()
    except Exception as e:
        log_error(f"Error in update_cymatic_pattern: {e}\n{traceback.format_exc()}")
        raise

def cymatics_pattern(frequency, grid_size=100, amplitude=1):
    Z = amplitude * np.sin(frequency * np.sqrt(X**2 + Y**2))
    return Z

def log_error(message):
    error_text.insert(tk.END, message + "\n")
    error_text.see(tk.END)

def on_select(eventpress, eventrelease):
    try:
        # Extract the coordinates from the events
        x0, y0 = eventpress.xdata, eventpress.ydata
        x1, y1 = eventrelease.xdata, eventrelease.ydata
        
        # Generate and display the cropped cymatic pattern
        pattern = cymatics_pattern(frequency_slider.get())
        cropped_pattern = pattern[int(y0):int(y1), int(x0):int(x1)]
        ax.clear()
        ax.imshow(cropped_pattern, cmap='viridis', extent=(x0, x1, y0, y1))
        ax.set_title(f'Cymatic Pattern (Cropped) at {frequency_slider.get()} Hz')
        ax.set_facecolor('black')
        ax.set_xticks([])  # Hide the x-axis
        ax.set_yticks([])  # Hide the y-axis
        ax.set_zticks([])  # Hide the z-axis
        canvas.draw()
    except Exception as e:
        log_error(f"Error in on_select: {e}\n{traceback.format_exc()}")
        raise

def animate(frame):
    try:
        # Adjust the pattern to create an animation effect
        pattern = cymatics_pattern(frequency_slider.get() + frame * 0.1)
        ax.clear()
        ax.plot_surface(X, Y, pattern, cmap='viridis')
        ax.set_title(f'Cymatic Pattern at {frequency_slider.get()} Hz')
        ax.set_facecolor('black')
        ax.set_xticks([])  # Hide the x-axis
        ax.set_yticks([])  # Hide the y-axis
        ax.set_zticks([])  # Hide the z-axis
        # Centering the logo
        ax.text2D(0.5, 0.95, "SOUNDFR3QK", transform=ax.transAxes, fontsize=24, color='orange', alpha=0.5, ha='center')
    except Exception as e:
        log_error(f"Error in animate: {e}\n{traceback.format_exc()}")
        raise

def increment_frequency():
    current_frequency = frequency_slider.get()
    frequency_slider.set(current_frequency + 1)

def decrement_frequency():
    current_frequency = frequency_slider.get()
    frequency_slider.set(current_frequency - 1)

# Create the main window
root = tk.Tk()
root.title("Rife Frequency Player")
root.configure(bg='black')

# Create and place the frequency dropdown
frequency_label = ttk.Label(root, text="Select Frequency:", foreground='green', background='black')
frequency_label.pack(pady=5)

frequency_combo = ttk.Combobox(root, values=list(frequencies.keys()))
frequency_combo.pack(pady=5)
frequency_combo.bind("<<ComboboxSelected>>", update_description)

# Create and place the description label
description_label = ttk.Label(root, text="", wraplength=300, foreground='green', background='black')
description_label.pack(pady=5)

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
selector = RectangleSelector(ax, on_select, useblit=True, button=[1], minspanx=5, minspany=5, spancoords='pixels', interactive=True)

# Start the tkinter main loop
root.mainloop()
