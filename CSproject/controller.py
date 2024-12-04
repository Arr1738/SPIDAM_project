# Controls logic between view and model

from model import load_audio, calculate_rt60, calculate_band_rt60


class Controller:
    def __init__(self, view):
        self.view = view
        self.audio_file = None
        self.sample_rate = None
        self.rt60_value = None
        self.duration = None

    def load_audio_file(self, file_path):
        #load audio file using model and pass to view
        print(f"Loading audio file: {file_path}")
        self.audio_file, self.sample_rate = load_audio(file_path)

        if self.audio_file is not None:
            #audio duration (seconds)
            self.duration = len(self.audio_file) / self.sample_rate
            print(f"Audio duration: {self.duration:.2f} seconds")

            #call calculation after loading audio
            self.rt60_value = calculate_rt60(self.audio_file, self.sample_rate)

            #calculate rt60 for low, mid, and high frequencies
            self.band_rt60_values = calculate_band_rt60(self.audio_file, self.sample_rate)

            if self.rt60_value is None:
                print("RT60 calculation failed. Ensure the audio file has a clear decay")
                self.view.update_rt60_value(None)
            else:
                print(f"Calculated RT60: {self.rt60_value:.2f} seconds")
                print(f"Band-specific RT60 values: {self.band_rt60_values}")
                self.view.update_rt60_value(self.rt60_value)

            #update view with calculated rt60 value
            self.view.update_audio_info(file_path, self.duration)
            self.view.update_audio_data(self.audio_file, self.sample_rate)

    def plot_rt60(self):
        #plot rt60 data in view file
        if self.rt60_value is not None:
            print(f"Plotting RT60: {self.rt60_value:.2f} seconds")
            #generate plot using calculated rt60 value
            self.view.plot_rt60(self.rt60_value)
        else:
            print('RT60 value is not calculated yet.')

    def clear_plot(self):
        #clear plot from view
        self.view.clear_plot()

    def save_plot(self):
        #save plot to a file
        if self.rt60_value is not None:
            print(f"Saving RT60 plot with value: {self.rt60_value:.2f} seconds")
            self.view.save_plot(self.rt60_value)
        else:
            print('RT60 value is not calculated yet.')
