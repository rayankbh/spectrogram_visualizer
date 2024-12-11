# Real-Time Audio Spectrogram Visualizer

This repository contains a Python-based real-time audio spectrogram visualizer. Using a microphone input, the application performs a Short-Time Fourier Transform (STFT) on incoming audio data and displays the resulting frequency spectrum as a scrolling spectrogram in real time.  

**Key Features:**
- Captures audio from your default microphone.
- Applies a windowed FFT to generate a spectrogram.
- Displays the spectrogram continuously, updating every few milliseconds.
- Uses a fixed dB range and custom colormap for a visually consistent output.
- Adjustable parameters for frequency resolution, latency, and visual styling.

## Requirements

**Python Version:**  
Python 3.8 or newer is recommended.

**Dependencies:**  
- [sounddevice](https://pypi.org/project/sounddevice/)
- [librosa](https://pypi.org/project/librosa/)
- [matplotlib](https://pypi.org/project/matplotlib/)
- [numpy](https://pypi.org/project/numpy/)
- [tkinter](https://docs.python.org/3/library/tkinter.html) (generally included with Python on most platforms; on Linux, you may need to install `python3-tk`)

**PortAudio Dependency:**  
`sounddevice` relies on PortAudio.  
- On Ubuntu/Debian:  
  ```bash
  sudo apt-get update
  sudo apt-get install libportaudio2 portaudio19-dev
  ```
- On macOS with Homebrew:  
  ```bash
  brew install portaudio
  ```
- On Windows, `pip install sounddevice` usually includes the necessary binaries by default.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/realtime-audio-spectrogram.git
   cd realtime-audio-spectrogram
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```
   *On Windows (PowerShell or CMD):*
   ```powershell
   python -m venv env
   .\env\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the script:**
   ```bash
   python realtime_spectrogram.py
   ```

## Usage

- **Start Recording:** Click the **"Start Recording"** button. The spectrogram will begin to update as it receives audio from your microphone.
- **Stop Recording:** Click the **"Stop Recording"** button to stop the microphone stream.
- **Visual Output:** The spectrogram scrolls horizontally over time. Frequency bins are shown on the vertical axis and time frames on the horizontal axis.  
  - Louder sounds at particular frequencies appear as brighter colors (toward yellow/red).
  - Quieter sounds or silence appear as darker colors (blue/black).

**Tips:**
- Make sure your microphone is not muted and that Python has permission to access it.
- Experiment with making different sounds (talk, clap, whistle) to see variations in the spectrogram.
- Adjust parameters (`N_FFT`, `BLOCK_SIZE`, `set_clim()` range) in the code to improve clarity, resolution, and latency.

## Parameters to Experiment With

- `N_FFT`: Increasing this provides finer frequency resolution but requires more computation.
- `BLOCK_SIZE`: Smaller blocks reduce latency but increase CPU load.
- Colormap and `set_clim()`: Adjust the dynamic range of the spectrogram’s display.
- Sample Rate: Can be changed depending on your microphone’s capabilities, although 44100 Hz is standard.

## Troubleshooting

- **Blank or Uniform Spectrogram:**  
  Ensure you are producing sound. If it’s still uniform, try adjusting the `set_clim()` values or check that the microphone input device is correct.
  
- **High Latency or Stuttering:**  
  Reduce `BLOCK_SIZE` or decrease `N_FFT`. Ensure that your system can handle real-time FFT computations.

- **Microphone Not Working:**  
  Check `sd.query_devices()` in a Python shell to list input devices and specify the `device` parameter in `InputStream` if needed.

## License

This project is released under the [MIT License](LICENSE).

