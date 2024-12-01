# Manages GUI
# Displays plots and controls for file import

import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SPIDAMpp:
    def __init__(self, root):
        self.root = root
        self.root.title("SPIDAM - Reverberation Time Analysis")
        self.create_widgets()

    def create_widgets(self):
        #load button
        self.load_button = tk.Button(self.root, text="Load Audio File", command=self.load_file)
        self.load_button.pack(pady=10)

        #plot button
        self.plot_button = tk.Button(self.root, text="Plot RT60", command=self.plot_rt60)
        self.plot_button.pack(pady=10)

        #canvas for displaying plots
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(pady=10)

    def load_file(self):
        #open file dialog to load audio file
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav"), ("MP3 files", "*.mp3")])
        if file_path:
            print(f"Loaded file: {file_path}")

    def plot_rt60(self):
        #plots dummy graph for now
        fig, ax = plt.subplots()
        ax.plot([0, 1, 2, 3, 4], [0, 1, 0, 1, 0]) # dummy data, replace with actual rt60 data
        ax.set_title('RT60 Plot')
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel("RT60 (s)")

        #embed plot in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = SPIDAMpp(root)
    root.mainloop()

