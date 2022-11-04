import tkinter as tk


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        """This is the base class for all pages"""
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        """THis function shows the page on the same window"""
        self.lift()
