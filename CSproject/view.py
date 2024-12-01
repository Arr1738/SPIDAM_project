# Manages GUI
# Displays plots and controls for file import
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from model import load_audio, calculate_rt60
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

class SPIDAMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SPIDAM - Reverberation Time Analysis")
        self.save_plot = None
        self.audio_file = None
        self.sample_rate = None
        self.audio_info_label = None
        self.rt60_value = None
        self.create_widgets()

    def create_widgets(self):
        # Load Button
        self.load_button = tk.Button(self.root, text="Load Audio File", command=self.load_file)
        self.load_button.pack(pady=10)

        # Plot Button
        self.plot_button = tk.Button(self.root, text="Plot RT60", command=self.plot_rt60)
        self.plot_button.pack(pady=10)

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
            self.audio_file, self.sample_rate = load_audio(file_path)

            #audio duration
            duration = len(self.audio_file / self.sample_rate)

            if self.audio_file is not None:
                self.rt60_value = calculate_rt60(self.audio_file, self.sample_rate)
                self.rt60_label.config(text=f"RT60 Value: {self.rt60_value:.2f} s")  # Update RT60 value display
                #display file info
                self.audio_info_label.config(text=f"File: {file_path.split('/')[-1]} | Duration: {duration:.2f}s")
                print(f"RT60 Value: {self.rt60_value}")

    def plot_rt60(self):
        if self.rt60_value is not None:
            # Clear any existing plot
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()

            frequencies = [100, 500, 1000, 2000, 4000, 8000]  # Example frequencies in Hz
            rt60_values = [self.rt60_value * 0.8, self.rt60_value * 0.9, self.rt60_value * 1.0,
                           self.rt60_value * 1.2, self.rt60_value * 1.4, self.rt60_value * 1.6]  # Example RT60 for each frequency

            # Create the Matplotlib figure
            fig, ax = plt.subplots(figsize=(6, 4))

            # Plot the data
            ax.plot(frequencies, rt60_values, marker='o', linestyle='-', color='b', label="RT60 Values")
            ax.set_title(f"RT60 Plot - {self.rt60_value:.2f} s")
            ax.set_xlabel("Frequency (Hz)")
            ax.set_ylabel("RT60 (s)")
            ax.legend()

            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()

            #Pack the canvas widget to display the plot
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        else:
            print("Please load an audio file first.")

    #save plots
    def save_plot(self):
        if self.rt60_value is not None:
            #Save the current plot as a PNG file
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot([100, 500, 1000, 2000, 4000, 8000],
                    [self.rt60_value * 0.9, self.rt60_value * 1.0, self.rt60_value * 1.1,
                     self.rt60_value * 1.2, self.rt60_value * 1.4, self.rt60_value * 1.6], marker='o', color='b')
            ax.set_title(f"RT60 Plot - {self.rt60_value:.2f} s")
            ax.set_xlabel("Frequency (Hz)")
            ax.set_ylabel("RT60 (s)")

            #Save as PNG
            fig.savefig('rt60_plot.png')
            print("Plot saved as rt60_plot.png")

    # Remove any existing plot from the canvas
    def clear_plot(self):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        print("Plot cleared.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SPIDAMApp(root)
    root.mainloop()
