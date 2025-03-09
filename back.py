import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk

class Knight:
    def __init__(self):
        self.position = (0, 0)  # Position initiale
        self.assignment = []  # Liste des mouvements appliqués
        self.path = [self.position]  # Chemin emprunté par le cavalier

    def move_forward(self, direction):
        moves = [
            (-2, 1), (-1, 2), (1, 2), (2, 1),
            (2, -1), (1, -2), (-1, -2), (-2, -1)
        ]
        dx, dy = moves[direction - 1]
        return (self.position[0] + dx, self.position[1] + dy)

    def move_backward(self):
        if self.assignment:
            self.assignment.pop()
            self.path.pop()
            self.position = self.path[-1]

    def consistent(self, direction):
        new_position = self.move_forward(direction)
        x, y = new_position
        return (
            0 <= x < 8 and 0 <= y < 8 and new_position not in self.path
        )

    def add_move(self, direction):
        self.assignment.append(direction)
        self.position = self.move_forward(direction)
        self.path.append(self.position)

    def remove_move(self):
        self.move_backward()


def backtracking(knight):
    if len(knight.path) == 64:  # Si toutes les cases sont visitées
        return knight
    for direction in range(1, 9):  # Explorer chaque direction
        if knight.consistent(direction):
            knight.add_move(direction)
            result = backtracking(knight)
            if result:
                return result
            knight.remove_move()  # Retour sur trace
    return None


class KnightTourGUI:
    def __init__(self, knight):
        self.knight = knight
        self.window = tk.Tk()
        self.window.title("Tour du Cavalier - Solution")

        self.cell_size = 60
        self.board_size = 8
        self.canvas = Canvas(self.window, width=self.cell_size * self.board_size, height=self.cell_size * self.board_size)
        self.canvas.pack()

        # Dessiner le damier
        for i in range(self.board_size):
            for j in range(self.board_size):
                color = 'white' if (i + j) % 2 == 0 else 'gray'
                self.canvas.create_rectangle(
                    j * self.cell_size, i * self.cell_size,
                    (j + 1) * self.cell_size, (i + 1) * self.cell_size,
                    fill=color
                )

        # Charger l'image du cavalier
        self.knight_image = Image.open("bN.png")
        self.knight_image = self.knight_image.resize((self.cell_size, self.cell_size), Image.Resampling.LANCZOS)
        self.knight_image_tk = ImageTk.PhotoImage(self.knight_image)

        self.step_count = 0
        self.visited_squares = set()
        self.square_number = 1

        # Bouton pour relancer
        self.reset_button = tk.Button(self.window, text="Relancer", command=self.reset_and_start)
        self.reset_button.pack()

        # Slider pour contrôler la vitesse
        self.speed_slider = tk.Scale(self.window, from_=100, to=2000, label="Vitesse d'animation (ms)", orient="horizontal")
        self.speed_slider.set(500)
        self.speed_slider.pack()

        self.animate_moves()

    def animate_moves(self):
        if self.step_count < len(self.knight.path):
            x, y = self.knight.path[self.step_count]

            # Ajouter le numéro de la case visitée
            if (x, y) not in self.visited_squares:
                self.canvas.create_text(
                    y * self.cell_size + self.cell_size // 2,
                    x * self.cell_size + self.cell_size // 2,
                    text=str(self.square_number), font=("Arial", 12)
                )
                self.visited_squares.add((x, y))
                self.square_number += 1

            # Afficher l'image du cavalier
            if self.step_count == 0:
                self.knight_marker = self.canvas.create_image(
                    y * self.cell_size + self.cell_size // 2,
                    x * self.cell_size + self.cell_size // 2,
                    image=self.knight_image_tk
                )
            else:
                self.canvas.coords(
                    self.knight_marker,
                    y * self.cell_size + self.cell_size // 2,
                    x * self.cell_size + self.cell_size // 2
                )

            self.step_count += 1
            delay = self.speed_slider.get()
            self.window.after(delay, self.animate_moves)

    def reset_and_start(self):
        self.canvas.delete("all")
        for i in range(self.board_size):
            for j in range(self.board_size):
                color = 'white' if (i + j) % 2 == 0 else 'gray'
                self.canvas.create_rectangle(
                    j * self.cell_size, i * self.cell_size,
                    (j + 1) * self.cell_size, (i + 1) * self.cell_size,
                    fill=color
                )

        self.step_count = 0
        self.visited_squares.clear()
        self.square_number = 1
        self.animate_moves()

    def run(self):
        self.window.mainloop()


def main():
    knight = Knight()
    solution = backtracking(knight)
    if solution:
        print("Tour du cavalier trouvé !")
        print("Séquence des mouvements :", solution.assignment)
        print("Chemin :", solution.path)
        gui = KnightTourGUI(solution)
        gui.run()
    else:
        print("Pas de solution trouvée.")


if __name__ == "__main__":
    main()
