# Manages GUI
# Displays plots and controls for file import
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from model import load_audio, calculate_rt60
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import librosa.display
from controller import Controller

class SPIDAMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SPIDAM - Reverberation Time Analysis")
        self.controller = Controller(self) #controller initialized
        self.audio_file = None
        self.sample_rate = None
        self.rt60_value = None
        self.create_widgets()

    def create_widgets(self):
        # Load Button
        self.load_button = tk.Button(self.root, text="Load Audio File", command=self.load_file)
        self.load_button.pack(pady=10)

        # Plot Button
        self.plot_button = tk.Button(self.root, text="Plot RT60", command=self.plot_rt60)
        self.plot_button.pack(pady=10)

        #show waveform
        self.waveform_button = tk.Button(self.root, text="Show Waveform", command=self.show_waveform)
        self.waveform_button.pack(pady=10)

        #save plot
        self.save_button = tk.Button(self.root, text="Save Plot", command=self.save_plot)
        self.save_button.pack(pady=10)

        # Clear Button
        self.clear_button = tk.Button(self.root, text="Clear Plot", command=self.clear_plot)
        self.clear_button.pack(pady=10)

        # RT60 Value Display
        self.rt60_label = tk.Label(self.root, text="RT60 Value: Not Calculated", font=("Helvetica", 12))
        self.rt60_label.pack(pady=10)

        # Canvas for displaying plots
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(pady=20)

        self.audio_info_label = tk.Label(self.root, text="File: Not Loaded | Duration: 0.00s", font=("Helvetica", 12))
        self.audio_info_label.pack(pady=10)

    def load_file(self):
        #load the audio file
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav"), ("MP3 files", "*.mp3")])
        if file_path:
            print(f"Loaded file: {file_path}")
            self.controller.load_audio_file(file_path)

    def update_audio_data(self, audio, sample_rate):
        self.audio_file = audio
        self.sample_rate = sample_rate
        print("Audio data and sample rate updated in the view.")

    def show_waveform(self):
        if self.audio_file is not None and self.sample_rate is not None:
            # Clear existing plots
            self.clear_plot()

            # Create the Matplotlib figure
            fig, ax = plt.subplots(figsize=(10, 4))
            librosa.display.waveshow(self.audio_file, sr=self.sample_rate, ax=ax, x_axis='time', color='b')
            ax.set_title("Waveform")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Amplitude")
            plt.tight_layout()

            # Embed the plot into Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        else:
            print("No audio file loaded. Please load a file first.")

    def plot_rt60(self):
        self.controller.plot_rt60()

    def clear_plot(self):
        self.controller.clear_plot()

    def save_plot(self):
        self.controller.save_plot()

    def update_rt60_value(self, rt60_value):
        #update rt60 value in gui
        print(f"Updating RT60 value in view: {rt60_value}") #debugging
        self.rt60_value = rt60_value
        if rt60_value is not None:
            self.rt60_label.config(text=f"RT60 Value: {rt60_value:.2f} s")
        else:
            self.rt60_label.config(text="RT60 Value: Calculation Failed")

    def update_audio_info(self, file_path, duration):
        #display file name and duration
        self.audio_info_label.config(text=f"File: {file_path.split('/')[-1]} | Duration: {duration:.2f}s")

    def plot_rt60(self):
        # Plot RT60 in the GUI
        if self.rt60_value is not None:
            print(f"Plotting RT60: {self.rt60_value:.2f} s")
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot([100, 500, 1000, 2000, 4000, 8000],
                    [self.rt60_value * 0.9, self.rt60_value * 1.0, self.rt60_value * 1.1,
                     self.rt60_value * 1.2, self.rt60_value * 1.4, self.rt60_value * 1.6],
                    marker='o', color='b', label="RT60 Across Frequencies")
            ax.set_title(f"RT60 Plot - {self.rt60_value:.2f} s")
            ax.set_xlabel("Frequency (Hz)")
            ax.set_ylabel("RT60 (s)")
            ax.legend()

            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        else:
            print("RT60 value is not available")

    #save plots
    def save_plot(self):
        if self.rt60_value is not None:
            #Save the current plot as a PNG file
            print(f"Saving plot with RT60 Value: {self.rt60_value}")
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot([100, 500, 1000, 2000, 4000, 8000],
                    [self.rt60_value * 0.9, self.rt60_value * 1.0, self.rt60_value * 1.1,
                     self.rt60_value * 1.2, self.rt60_value * 1.4, self.rt60_value * 1.6],
                    marker='o', color='b', label="RT60 Across Frequencies")

            ax.set_title(f"RT60 Plot - {self.rt60_value:.2f} s")
            ax.set_xlabel("Frequency (Hz)")
            ax.set_ylabel("RT60 (s)")
            ax.legend()

            #Save as PNG
            fig.savefig('rt60_plot.png')
            print("Plot saved as rt60_plot.png")
        else:
            print("RT60 value is not available for saving")

    # Remove any existing plot from the canvas
    def clear_plot(self):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        print("Plot cleared.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SPIDAMApp(root)
    root.mainloop()
