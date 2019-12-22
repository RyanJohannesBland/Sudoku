from dataclasses import dataclass, field
import tkinter as tk
import random


W = 75
H = 75


@dataclass
class Node:
    val: int = 0
    options: list = field(default_factory=list)


class UI:

    def __init__(self):
        # Set up window and canvas.
        self.window = tk.Tk()
        self.window.title("Sudoku")
        self.window.geometry("675x675")
        self.canvas = tk.Canvas(self.window, bg="white", height=675, width=675)
        self.canvas.pack()
        # Set up nodes
        self.nodes = self._create_nodes()
        # Draw initial gameboard
        self._draw_grid()
        self._draw_board()

    def _create_nodes(self):
        nodes = list()
        for i in range(9):
            row = list()
            for val in range(9):
                row.append(Node(0, [i for i in range(1,10)]))
            nodes.append(row)
        return nodes

    def _draw_node(self, y, x):
        self.canvas.create_rectangle(
            x * W, y * H, x * W + W, y * H + H, fill="white")
        node = self.nodes[y][x]
        if node.val == 0:
            for val in node.options:
                self.canvas.create_text(
                    ((val - 1) % 3) * (W // 3) + (x * W) + 10,
                    ((val - 1) // 3) * (H // 3) + (y * H) + 10,
                    text=val,
                    font="Times 18")
        else:
            self.canvas.create_text(
                x * W + 35, y * H + 35, text=node.val, font="Times 48")

    def _draw_grid(self):
        for i in range(1, 9):
            self.canvas.create_line(W * i, 0, W * i, H * 9)
            self.canvas.create_line(0, H * i, W * 9, H * i)

    def _draw_board(self):
        for i in range(9):
            for j in range(9):
                self._draw_node(i, j)

    def set_value(self, y, x, val):
        self.nodes[y][x].val = val
        for x_val in range(len(self.nodes[y])):
            try:
                self.nodes[y][x_val].options.remove(val)
                self._draw_node(y, x_val)
            except ValueError:
                pass
        for y_val in range(len(self.nodes)):
            try:
                self.nodes[y_val][x].options.remove(val)
                self._draw_node(y_val, x)
            except ValueError:
                pass
        for i in range(3):
            for j in range(3):
                try:
                    x_val = j + x // 3 * 3
                    y_val = i +  y // 3 * 3
                    self.nodes[y_val][x_val].options.remove(val)
                    self._draw_node(y_val, x_val)
                except ValueError:
                    pass
        self._draw_node(y, x)

def main():
    ui = UI()
    ui.set_value(2, 2, 2)
    ui.set_value(7, 3, 9)
    ui.window.mainloop()


def algorithm(ui):
    pass


if __name__ == "__main__":
    main()