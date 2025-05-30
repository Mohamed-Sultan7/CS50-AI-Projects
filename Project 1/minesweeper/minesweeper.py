import itertools
import random


class Minesweeper():
    def __init__(self, height=8, width=8, mines=8):
        self.height = height
        self.width = width
        self.mines = set()
        self.board = [[False for _ in range(self.width)] for _ in range(self.height)]

        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        self.mines_found = set()

    def print(self):
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                print("|X" if self.board[i][j] else "| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        count = 0
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1
        return count

    def won(self):
        return self.mines_found == self.mines


class Sentence():
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        if len(self.cells) == self.count and self.count > 0:
            return set(self.cells)
        return set()

    def known_safes(self):
        if self.count == 0:
            return set(self.cells)
        return set()

    def mark_mine(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    def __init__(self, height=8, width=8):
        self.height = height
        self.width = width
        self.moves_made = set()
        self.mines = set()
        self.safes = set()
        self.knowledge = []

    def mark_mine(self, cell):
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        self.moves_made.add(cell)
        self.mark_safe(cell)

        neighbors = set()
        i, j = cell
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                ni, nj = i + di, j + dj
                if (ni, nj) == cell or ni < 0 or nj < 0 or ni >= self.height or nj >= self.width:
                    continue
                if (ni, nj) in self.safes:
                    continue
                if (ni, nj) in self.mines:
                    count -= 1
                    continue
                neighbors.add((ni, nj))

        if neighbors:
            self.knowledge.append(Sentence(neighbors, count))

        changed = True
        while changed:
            changed = False
            safes = set()
            mines = set()

            for sentence in self.knowledge:
                safes |= sentence.known_safes()
                mines |= sentence.known_mines()

            for safe in safes:
                if safe not in self.safes:
                    self.mark_safe(safe)
                    changed = True

            for mine in mines:
                if mine not in self.mines:
                    self.mark_mine(mine)
                    changed = True

            new_knowledge = []
            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    if s1 == s2 or not s1.cells or not s2.cells:
                        continue
                    if s1.cells.issubset(s2.cells):
                        diff = s2.cells - s1.cells
                        diff_count = s2.count - s1.count
                        new_sentence = Sentence(diff, diff_count)
                        if new_sentence not in self.knowledge and new_sentence not in new_knowledge:
                            new_knowledge.append(new_sentence)
            self.knowledge.extend(new_knowledge)

    def make_safe_move(self):
        for move in self.safes:
            if move not in self.moves_made:
                return move
        return None

    def make_random_move(self):
        for i in range(self.height):
            for j in range(self.width):
                move = (i, j)
                if move not in self.moves_made and move not in self.mines:
                    return move
        return None
