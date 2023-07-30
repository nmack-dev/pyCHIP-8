import tkinter as tk

class EmulatorUI:

    SIZE = 10

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CHIP-8 Emulator")
        self.root.geometry("640x320")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, width=640, height=320, bg="black")
        self.canvas.pack()

        for y in range(32):
            for x in range(64):
                self.canvas.create_rectangle(x * self.SIZE, y * self.SIZE, x * self.SIZE + self.SIZE, y * self.SIZE + self.SIZE, fill="black", outline="black")
    
    
    def draw_pixel(self, x, y, val):
        if val == 1:
            self.canvas.itemconfig(self.canvas.find_closest(x * self.SIZE + self.SIZE / 2, y * self.SIZE + self.SIZE / 2), fill="white")
        else:
            self.canvas.itemconfig(self.canvas.find_closest(x * self.SIZE + self.SIZE / 2, y * self.SIZE + self.SIZE / 2), fill="black")

        self.root.update()
    