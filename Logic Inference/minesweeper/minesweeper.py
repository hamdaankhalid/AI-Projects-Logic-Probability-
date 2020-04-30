import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()
        self.next_move = ()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells

        else:
            return {()}

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:

            return {()}

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells :
            # remove cell
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            # remove cell
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

        self.all_cells = []
        for i in range(8):
            for j in range(8):
                self.all_cells.append((i, j))

        print(self.all_cells)

    def near_by_mines(self, cell):
        #cell in corner or not in corner
        i, j = cell
        above = (i-1, j)
        above_right = (i-1, j+1)
        same_right = (i, j+1)
        below_right = (i+1, j+1)
        below = (i+1, j)
        below_left = (i+1, j-1)
        left_same = (i, j-1)
        left_above = (i-1, j-1)

        neighbors = [above, above_right, same_right, below_right, below, below_left, left_same, left_above]
        for i in neighbors:
            if list(i)[0] > 7 or list(i)[1] > 7:
                neighbors.remove(i)

        return neighbors

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # we are given a cell, see how this changes stuff for us
        self.moves_made.add(cell)
        # add all safes from that cell to mark_safe
        self.mark_safe(cell)

        # cell is a cell and count is number of mines around it
        new_sentence = Sentence(self.near_by_mines(cell), count)
        self.knowledge.append(new_sentence)

        for sentences in self.knowledge.copy():
           # check for safes or mines
            new_safes = sentences.known_safes().copy()
            new_mines = sentences.known_mines().copy()

            for i in new_safes:
                self.mark_safe(i)

            for j in new_mines:
                self.mark_mine(j)

        # add any new sentence inferences made
        for sentence in self.knowledge.copy():

            if new_sentence.cells.issubset(sentence.cells) or sentence.cells.issubset(new_sentence.cells):
                self.knowledge.append(Sentence(sentence.cells - new_sentence.cells, sentence.count - new_sentence.count))

            elif sentence.cells.issubset(new_sentence.cells):
                self.knowledge.append(Sentence(new_sentence.cells - sentence.cells ,new_sentence.count -  sentence.count))

            # check for safes or mines after new inference
            new_safes = sentence.known_safes()
            new_mines = sentence.known_mines()

            for i in new_safes.copy():
                self.mark_safe(i)

            for j in new_mines.copy():
                self.mark_mine(j)

# TODO
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        #find known safes in the entire database
        """    known safes(self):
                Returns the set of all cells in self.cells known to be safe where self is a sentence
                """
        #find intersection of set such that safe move and not made
        # possible_moves = self.safes.intersection(set(self.all_cells) - self.moves_made)
        # if possible_moves != set():
        #     return possible_moves.pop()

        for i in self.safes:
            if i in self.all_cells and i not in self.moves_made:
                return i
        
        

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        all_cell = random.choice(self.all_cells)

        while all_cell in self.moves_made:
            random_choices = (list(set(self.all_cells) - set(self.mines)))
            all_cell = random.choice(random_choices)

        return all_cell






