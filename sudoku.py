from dataclasses import dataclass, field
import tkinter as tk
import random
import argparse


W = 75
H = 75


@dataclass
class Node:
    y: int
    x: int
    val: int = 0
    options: list = field(default_factory=list)


class UI:

    def __init__(self, file=None):
        # Set up window and canvas.
        self.window = tk.Tk()
        self.window.title("Sudoku")
        self.window.geometry("675x675")
        self.canvas = tk.Canvas(self.window, bg="white", height=675, width=675)
        self.canvas.pack()
        # Set up nodes
        self.nodes = self._create_nodes()
        if file:
            self._read_file(file)
        # Draw initial gameboard
        self._draw_grid()
        self._draw_board()

    def _create_nodes(self):
        nodes = list()
        for y in range(9):
            row = list()
            for x in range(9):
                row.append(Node(y, x, 0, [i for i in range(1,10)]))
            nodes.append(row)
        return nodes

    def _read_file(self, file):
        with open(file) as f:
            f = f.readlines()

            try:
                assert len(f) == 9
                for y in range(len(f)):
                    f[y] = f[y].strip()
                    assert len(f[y]) == 9
                    for x in range(len(f[y])):
                        if int(f[y][x]) > 0:
                            self.set_value(self.nodes[y][x], int(f[y][x]))
            except AssertionError:
                print("caught an error")

    def _draw_node(self,node):
        x = node.x
        y = node.y
        self.canvas.create_rectangle(
            x * W, y * H, x * W + W, y * H + H, fill="white")
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
                self._draw_node(self.nodes[i][j])

    def set_value(self, node, val):
        node.val = val
        x = node.x
        y = node.y
        for n in self.nodes[y]:
            try:
                n.options.remove(val)
                self._draw_node(n)
            except ValueError:
                pass
        for y_val in range(len(self.nodes)):
            try:
                self.nodes[y_val][x].options.remove(val)
                self._draw_node(self.nodes[y_val][x])
            except ValueError:
                pass
        for i in range(3):
            for j in range(3):
                try:
                    x_val = j + x // 3 * 3
                    y_val = i +  y // 3 * 3
                    self.nodes[y_val][x_val].options.remove(val)
                    self._draw_node(self.nodes[y_val][x_val])
                except ValueError:
                    pass
        self._draw_node(node)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", dest="file",default=None)
    args = parser.parse_args()

    ui = UI(file=args.file)
    ui.window.mainloop()

    algorithm(ui)


def algorithm(ui):
    while True:
        for row in len(ui.nodes):
            val_options = dict()
            for col in len(ui.nodes[row]):
                for option in ui.nodes[row][col].options:
                    pass


if __name__ == "__main__":
    main()