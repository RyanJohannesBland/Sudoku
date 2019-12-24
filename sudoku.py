import tkinter as tk
from dataclasses import dataclass, field
import os
import time


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
        self.geometry("800x800")
        self.configure(background="blue")

        self.canvas = tk.Canvas(self, bg="white", height=675, width=675)
        self.canvas.grid(row=0, column=0, columnspan=3)

        options = ["1", "2", "3", "4", "5"]
        self.dropdown_choice = tk.StringVar(self)
        self.dropdown_choice.set(options[0])
        self.options_menu = tk.OptionMenu(self, self.dropdown_choice, *options)
        self.select_button = tk.Button(
            self, width=12, text="Load file", command=lambda: read_file(self))
        self.select_button.grid(row=2,column=0)
        self.options_menu.grid(row=3, column=0)

        self.algorithm_button = tk.Button(
            self, width=12, text="Algorithm", command=lambda: algorithm(self))
        self.algorithm_button.grid(row=2, column=2)

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
    gui.mainloop()


def create_nodes():
    NODES.clear()
    for y in range(9):
        row = list()
        for x in range(9):
            row.append(Node(y, x, 0, [i for i in range(1,10)]))
        NODES.append(row)


def read_file(gui):
    create_nodes()
    file_path = os.path.join(
        "example_files", f"example_{gui.dropdown_choice.get()}.txt")
    with open(file_path) as f:
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
    gui.draw_board()


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


# This algorithm performs a sweep of all nodes, checking for any nodes that are
# either A: the only viable choice for a given number, or B: that has only one
# possible option.
def algorithm(gui):
    for row in NODES:
        val_options = dict()
        for node in row:
            for option in node.options:
                val_options.setdefault(option, list())
                val_options[option].append(node)
        for option, nodes in val_options.items():
            if len(nodes) == 1 and nodes[0].val == 0:
                set_value(gui, nodes[0], option)
    for col in range(len(NODES[0])):
        val_options = dict()
        for row in NODES:
            for option in row[col].options:
                val_options.setdefault(option, list())
                val_options[option].append(row[col])
        for option, nodes in val_options.items():
            if len(nodes) == 1 and nodes[0].val == 0:
                set_value(gui, nodes[0], option)
    for y in range(3):
        for x in range(3):
            val_options = dict()
            for i in range(3):
                for j in range(3):
                    node = NODES[y * 3 + i][x * 3 + j]
                    for option in node.options:
                        val_options.setdefault(option, list())
                        val_options[option].append(node)
            for option, nodes in val_options.items():
                if len(nodes) == 1 and nodes[0].val == 0:
                    set_value(gui, nodes[0], option)
    for row in NODES:
        for node in row:
            if len(node.options) == 1 and node.val == 0:
                set_value(gui, node, node.options[0])


if __name__ == "__main__":
    main()