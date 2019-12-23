import tkinter as tk
from dataclasses import dataclass, field
import argparse


W = 75
H = 75
NODES = list()


@dataclass
class Node:
    y: int
    x: int
    val: int = 0
    options: list = field(default_factory=list)


class Graphics(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Sudoku")
        self.geometry("675x775")

        self.canvas = tk.Canvas(self, bg="white", height=675, width=675)
        self.canvas.grid(row=0, column=0)

        self.button = tk.Button(
            self, width=12, text="Click me", command=self.draw_board)
        self.button.grid(row=1, column=0)

        self.button2 = tk.Button(
            self, width=12, text="Click me 2", command=lambda: read_file(self))
        self.button2.grid(row=2, column=0)

    def draw_node(self, node):
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

    def draw_grid(self):
        for i in range(1, 9):
            self.canvas.create_line(W * i, 0, W * i, H * 9)
            self.canvas.create_line(0, H * i, W * 9, H * i)

    def draw_board(self):
        self.draw_grid()
        for i in range(9):
            for j in range(9):
                self.draw_node(NODES[i][j])


def main():
    gui = Graphics()

    create_nodes()

    gui.mainloop()


def create_nodes():
    for y in range(9):
        row = list()
        for x in range(9):
            row.append(Node(y, x, 0, [i for i in range(1,10)]))
        NODES.append(row)


def read_file(gui):
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", dest="file", default=None)
    args = parser.parse_args()
    with open(args.file) as f:
        f = f.readlines()
        try:
            assert len(f) == 9
            for y in range(len(f)):
                f[y] = f[y].strip()
                assert len(f[y]) == 9
                for x in range(len(f[y])):
                    if int(f[y][x]) > 0:
                        set_value(gui, NODES[y][x], int(f[y][x]))
        except AssertionError:
            print("caught an error")


def set_value(gui, node, val):
    node.val = val
    x = node.x
    y = node.y
    for n in NODES[y]:
        try:
            n.options.remove(val)
            gui.draw_node(n)
        except ValueError:
            pass
    for y_val in range(len(NODES)):
        try:
            NODES[y_val][x].options.remove(val)
            gui.draw_node(NODES[y_val][x])
        except ValueError:
            pass
    for i in range(3):
        for j in range(3):
            try:
                x_val = j + x // 3 * 3
                y_val = i +  y // 3 * 3
                NODES[y_val][x_val].options.remove(val)
                gui.draw_node(NODES[y_val][x_val])
            except ValueError:
                pass
    gui.draw_node(node)


if __name__ == "__main__":
    main()