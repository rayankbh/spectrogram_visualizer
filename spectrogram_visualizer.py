import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import queue

class AudioVisualizer:
    def __init__(self):
        self.SAMPLE_RATE = 44100
        self.BLOCK_SIZE = 1024
        self.N_FFT = 4096
        self.TIME_BINS = 100
        self.FREQ_BINS = self.N_FFT // 2 + 1

        # Spectrogram buffer
        self.spec_buffer = np.zeros((self.FREQ_BINS, self.TIME_BINS))

        # Audio data queue
        self.audio_queue = queue.Queue()
        self.running = False

        # Custom colormap; can choose whatever you want 
        colors = [(0, 0, 0),
                  (0, 0, 0.5),
                  (0, 0.5, 1),
                  (0, 1, 0),
                  (1, 1, 0),
                  (1, 0, 0)]
        self.colormap = LinearSegmentedColormap.from_list("custom", colors, N=100)

        # Set up the GUI
        self.setup_gui()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Real-Time Audio Spectrogram")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.fig.patch.set_facecolor('black')
        self.ax.set_facecolor('black')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Initialize spectrogram image
        self.img = self.ax.imshow(
            self.spec_buffer,
            aspect='auto',
            origin='lower',
            cmap=self.colormap,
            interpolation='nearest'
        )

        # Fix the color scale: -80 dB = dark, 0 dB = bright
        self.img.set_clim(-80, 0)

        self.ax.set_xlabel('Time Frames', color='white')
        self.ax.set_ylabel('Frequency Bins', color='white')
        self.ax.set_title('Real-Time Audio Spectrogram', color='white')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')

        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        self.start_button = tk.Button(button_frame, text="Start Recording", command=self.start_recording)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(button_frame, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

    def audio_callback(self, indata, frames, time_info, status):
        if status:
            print("Audio status:", status)
        self.audio_queue.put(indata.copy())

    def update_spectrogram(self):
        if self.running:
            while not self.audio_queue.empty():
                audio_data = self.audio_queue.get().flatten()

                # Windowing
                windowed = audio_data * np.hanning(len(audio_data))
                spectrum = np.fft.rfft(windowed, n=self.N_FFT)
                magnitude = np.abs(spectrum)

                # Convert to decibels relative to a small reference
                # No normalization here, just raw dB
                magnitude_db = 20 * np.log10(magnitude + 1e-10)

                # Shift spectrogram and add new column
                self.spec_buffer = np.roll(self.spec_buffer, -1, axis=1)
                self.spec_buffer[:, -1] = magnitude_db[:self.FREQ_BINS]

            # Update image without changing clim
            self.img.set_array(self.spec_buffer)
            self.canvas.draw()

            # Update again after 20 ms
            self.root.after(20, self.update_spectrogram)

    def start_recording(self):
        if not self.running:
            self.running = True
            self.stream = sd.InputStream(
                channels=1,
                samplerate=self.SAMPLE_RATE,
                blocksize=self.BLOCK_SIZE,
                callback=self.audio_callback
            )
            self.stream.start()
            self.update_spectrogram()
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            print("Recording started... Make sounds to see differences in the spectrogram.")

    def stop_recording(self):
        if self.running:
            self.running = False
            self.stream.stop()
            self.stream.close()
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            print("Recording stopped.")

    def on_closing(self):
        self.stop_recording()
        self.root.quit()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

def main():
    visualizer = AudioVisualizer()
    visualizer.run()

if __name__ == '__main__':
    main()
