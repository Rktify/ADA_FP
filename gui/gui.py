from pathlib import Path
from tkinter import *
from .Dijkstra import DijkstraAlgo
from .AStar import AStarAlgo

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def menuWindow():
    Menu()

class Menu(Toplevel):
    def __init__(self, *args, **kwargs):
        def goAstar():
            self.destroy()
            AStarAlgo.main()
        def goDijkstra():
            self.destroy()
            DijkstraAlgo.main()
        Toplevel.__init__(self, *args, **kwargs)
        self.title("Pathfinding Algorithm Menu")
        self.geometry("600x400")
        self.configure(bg = "#0063AB")

        self.canvas = Canvas(
            self,
            bg = "#0063AB",
            height = 400,
            width = 600,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.canvas.create_rectangle(
            0.0,
            75.0,
            600.0,
            109.0,
            fill="#80C2FF",
            outline="")

        self.canvas.create_rectangle(
            0.0,
            109.0,
            600.0,
            149.0,
            fill="#AFD5F8",
            outline="")

        self.canvas.create_rectangle(
            0.0,
            149.0,
            600.0,
            209.0,
            fill="#80C2FF",
            outline="")

        button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            self.canvas,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            activebackground="#0063AB",
            activeforeground="#0063AB"
        )
        self.button_1.place(
            x=20.0,
            y=221.0,
            width=559.0,
            height=154.0
        )

        button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        self.button_2 = Button(
            self.canvas,
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: goAstar(),
            relief="sunken",
            cursor="hand2"

        )
        self.button_2.place(
            x=321.0,
            y=241.0,
            width=136.0,
            height=114.0
        )

        button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        self.button_3 = Button(
            self.canvas,
            image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: goDijkstra(),
            relief="sunken",
            cursor="hand2"
        )
        self.button_3.place(
            x=143.0,
            y=241.0,
            width=136.0,
            height=114.0
        )

        self.canvas.create_text(
            89.0,
            5.0,
            anchor="nw",
            text="Pathfinding Algorithms",
            fill="#FFFFFF",
            font=("Encode Sans SC", 36 * -1)
        )

        self.canvas.create_text(
            223.0,
            70.0,
            anchor="nw",
            text="How to play:",
            fill="#000000",
            font=("Encode Sans SC", 25 * -1)
        )

        self.canvas.create_text(
            448.0,
            125.0,
            anchor="nw",
            text="Right Click: End Zone",
            fill="#000000",
            font=("Encode Sans SC", 11 * -1)
        )

        self.canvas.create_text(
            20.0,
            125.0,
            anchor="nw",
            text="Left Click: Starting Zone",
            fill="#000000",
            font=("Encode Sans SC", 11 * -1)
        )

        self.canvas.create_text(
            171.0,
            125.0,
            anchor="nw",
            text="Left Click (After placing start): Draw Obstacles",
            fill="#000000",
            font=("Encode Sans SC", 11 * -1)
        )

        self.canvas.create_text(
            132.0,
            161.0,
            anchor="nw",
            text="Backspace = Remove obstacles\nSpace = Remove endbox",
            fill="#000000",
            font=("Encode Sans SC", 11 * -1)
        )

        self.canvas.create_text(
            326.0,
            161.0,
            anchor="nw",
            text="R = Remove everything\nClose = Back to Main Menu",
            fill="#000000",
            font=("Encode Sans SC", 11 * -1)
        )

        self.canvas.create_text(
            239.0,
            110.0,
            anchor="nw",
            text="Enter: Start searching",
            fill="#000000",
            font=("Encode Sans SC", 11 * -1)
        )

        self.resizable(False, False)
        self.mainloop()