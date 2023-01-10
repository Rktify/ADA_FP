import tkinter as tk
from gui.gui import menuWindow

# Main window constructor
root = tk.Tk()  # Make temporary window for app to start
root.withdraw()  # WithDraw the window


if __name__ == "__main__":
    menuWindow()
    root.mainloop()