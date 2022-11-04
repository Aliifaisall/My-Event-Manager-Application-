from __future__ import annotations
import tkinter as tk


class LabelWidget:
    def __init__(
        self,
        screen: tk.Frame,
        text: str,
        type: str = "text",
        font: tuple = ("Arial", 10, "bold"),
        bg: str = "white",
    ) -> LabelWidget:
        """Simplified label widget

        Args:
            screen (_type_): The frame you want to place the label on
            text (str): The text you want to display
            type (str): Can be of type "title", "subtitle", "text"
            font (tuple, optional): Font to use for the label. Defaults to ("Arial", 10, "bold").
        """
        self.screen = screen
        self.text = text
        self.type = type
        self.bg = bg
        self.check_type()

    def check_type(self):
        """_summary_: This function is to check the type of the label and set the font accordingly

        Raises:
            ValueError: If an invalid type is passed it raises an error
        """
        if self.type == "title":
            self.font = ("Arial", 20, "bold")
        elif self.type == "subtitle":
            self.font = ("Arial", 15, "bold")
        elif self.type == "text":
            self.font = ("Arial", 10, "bold")
        else:
            raise ValueError("Invalid type")

    def place(self, x: int, y: int, width: int, height: int) -> None:
        """Place the label on the screen

        Args:
            x (int): Value for the X coordinate
            y (int): Value for the Y coordinate
            width (int): Width for the container
            height (int): Height for the container
        """
        self.label = tk.Label(self.screen, text=self.text, font=self.font, bg=self.bg)
        self.label.place(x=x, y=y, width=width, height=height)

    def place_rel(self, relx: int, rely: int, relwidth: int, relheight: int) -> None:
        """_summary_: Place the label on the screen using relative coordinates

        Args:
            relx (int): Relative x coordinate (0-1)
            rely (int): RELative y coordinate (0-1)
            relwidth (int): Relative width (0-1)
            relheight (int): ReLative height (0-1)
        """
        self.label = tk.Label(self.screen, text=self.text, font=self.font)
        self.label.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)

    def place_rel_size(self, x: int, y: int, relwidth: int, relheight: int) -> None:
        """_summary_: Place the label on the screen using relative coordinates"""
        self.label = tk.Label(self.screen, text=self.text, font=self.font)
        self.label.place(x=x, y=y, relwidth=relwidth, relheight=relheight)

    def place_rel_pos(self, relx: int, rely: int, width: int, height: int) -> None:
        """_summary_: Place the label on the screen using relative coordinates

        Args:
            relx (int): Relative x coordinate (0-1)
            rely (int): ReLative y coordinate (0-1)
            width (int): Width for the container
            height (int): Height for the container
        """
        self.label = tk.Label(self.screen, text=self.text, font=self.font)
        self.label.place(relx=relx, rely=rely, width=width, height=height)

    def grid(self, row, column, rowspan=1, columnspan=1, sticky="nsew"):
        self.label = tk.Label(self.screen, text=self.text, font=self.font)
        self.label.grid(
            row=row,
            column=column,
            sticky=sticky,
            rowspan=rowspan,
            columnspan=columnspan,
        )

    def pack(self, anchor="center", side=tk.LEFT):
        self.label = tk.Label(self.screen, text=self.text, font=self.font)
        self.label.pack(anchor=anchor, side=side)
