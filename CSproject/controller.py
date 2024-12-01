# Controls logic between view and model

from model import load_audio, calculate_rt60

class Controller:
    def __init__(self, view):
        self.view = view
        self.audio_file = None
        self.sample_rate = None
        self.rt60_value = None

    def load_audio(self, file_path):
        #load audio file using model and pass to view
        self.audio_file, self.sample_rate = load_audio(file_path)
        if self.audio_file is not None:
            #call calculation after loading audio
            self.rt60_value = calculate_rt60(self.audio_file, self.sample_rate)
            #update view with calculated rt60 value
            self.view.update_rt60_value(self.rt60_value)

    def plot_rt60(self):
        #plot rt60 data in view file
        if self.rt60_value is not None:
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
            self.view.save_plot(self.rt60_value)
        else:
            print('RT60 value is not calculated yet.')
