import sys
import copy
import random
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        return letter_grid(self.crossword, assignment)

    def print(self, assignment):
        print_board(self.letter_grid(assignment))

    def save(self, assignment, filename):
        image = self.letter_grid(assignment)
        save(image, filename)

    def solve(self):
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack({})

    def enforce_node_consistency(self):
        for var in self.domains:
            self.domains[var] = {word for word in self.domains[var] if len(word) == var.length}

    def revise(self, x, y):
        revised = False
        overlap = self.crossword.overlaps[x, y]
        if overlap is None:
            return False
        i, j = overlap
        to_remove = set()
        for xword in self.domains[x]:
            if not any(xword[i] == yword[j] for yword in self.domains[y]):
                to_remove.add(xword)
                revised = True
        self.domains[x] -= to_remove
        return revised

    def ac3(self, arcs=None):
        queue = list(arcs) if arcs is not None else [ (x, y) for x in self.domains for y in self.crossword.neighbors(x) ]
        while queue:
            x, y = queue.pop(0)
            if self.revise(x, y):
                if not self.domains[x]:
                    return False
                for z in self.crossword.neighbors(x) - {y}:
                    queue.append((z, x))
        return True

    def assignment_complete(self, assignment):
        return set(assignment.keys()) == self.crossword.variables

    def consistent(self, assignment):
        values = list(assignment.values())
        if len(set(values)) < len(values):
            return False
        for var in assignment:
            if len(assignment[var]) != var.length:
                return False
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    i, j = self.crossword.overlaps[var, neighbor]
                    if assignment[var][i] != assignment[neighbor][j]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        def conflicts(val):
            count = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment:
                    overlap = self.crossword.overlaps[var, neighbor]
                    if overlap:
                        i, j = overlap
                        count += sum(val[i] != w[j] for w in self.domains[neighbor])
            return count
        return sorted(self.domains[var], key=conflicts)

    def select_unassigned_variable(self, assignment):
        unassigned = [v for v in self.crossword.variables if v not in assignment]
        unassigned.sort(key=lambda var: (len(self.domains[var]), -len(self.crossword.neighbors(var))))
        return unassigned[0]

    def backtrack(self, assignment):
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result:
                    return result
        return None


def main():
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
