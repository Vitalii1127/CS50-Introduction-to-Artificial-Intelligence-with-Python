from crossword import Crossword, Variable
from PIL import Image, ImageDraw, ImageFont
import os


class CrosswordCreator():

    def __init__(self, crossword):
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("arial.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        for var in self.crossword.variables:
            self.domains[var] = {word for word in self.domains[var] if len(word) == var.length}

    def revise(self, x, y):
        revised = False
        overlap = self.crossword.overlaps[x, y]
        if overlap:
            i, j = overlap
            words = {word for word in self.domains[x] if i < len(word) and j < len(word) and any(word[i] == word[j] for word in self.domains[y])}
            if len(words) != len(self.domains[x]):
                self.domains[x] = words
                revised = True
        return revised

    def ac3(self, arcs=None):
        if arcs is None:
            arcs = [(x, y) for x in self.crossword.variables for y in self.crossword.neighbors(x)]
        while arcs:
            x, y = arcs.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x) - {y}:
                    arcs.append((z, x))
        return True

    def assignment_complete(self, assignment):
        return set(assignment.keys()) == set(self.crossword.variables)

    def consistent(self, assignment):
        for var1, word1 in assignment.items():
            if var1.length != len(word1):
                return False
            for var2, word2 in assignment.items():
                if var1 != var2:
                    overlap = self.crossword.overlaps[var1, var2]
                    if overlap:
                        i, j = overlap
                        if word1[i] != word2[j]:
                            return False
        return True

    def order_domain_values(self, var, assignment):
        values = []
        for value in self.domains[var]:
            count = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment and value in self.domains[neighbor]:
                    count += 1
            values.append((value, count))
        return [value for value, _ in sorted(values, key=lambda x: x[1])]

    def select_unassigned_variable(self, assignment):
        unassigned = [var for var in self.crossword.variables if var not in assignment]
        return min(unassigned, key=lambda var: (len(self.domains[var]), -len(self.crossword.neighbors(var))))

    def backtrack(self, assignment):
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
            del new_assignment[var]
        return None


def main():
    structure_path = "C:/Users/Vitalii/Desktop/CS50/crossword/data"
    words_path = "C:/Users/Vitalii/Desktop/CS50/crossword/data"
    output_image = "C:/Users/Vitalii/Desktop/CS50/crossword/data/output_image.png"
    crossword = Crossword(structure_path, words_path)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    if assignment is None:
        print("Рішення відсутнє.")
    else:
        creator.print(assignment)
        if output_image:
            creator.save(assignment, output_image)


if __name__ == "__main__":
    main()
