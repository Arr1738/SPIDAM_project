# Entry point for app
# initialize and launch GUI
import tkinter as tk
from view import SPIDAMApp

def main():
    #Create the main Tkinter root window
    root = tk.Tk()

    #Initialize the SPIDAM application
    app = SPIDAMApp(root)

    #Start the Tkinter main event loop
    root.mainloop()

if __name__ == "__main__":
    main()
