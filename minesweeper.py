import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=20):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

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

        # for i in range(5, 8):
        #     for j in range(4,7):
        #         self.board[i][j] = False
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
            print("Found Known Mines")
            return self.cells
        return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            print("Found Known Safes")
            return self.cells
        return None
        
    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        removable_set = set()
        for current_cell in self.cells:
            if current_cell == cell:
                removable_set.add(current_cell)
                self.count -= 1
        self.cells = self.cells - removable_set
    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        removable_set = set()
        for current_cell in self.cells:
            if current_cell == cell:
                removable_set.add(current_cell)

        self.cells = self.cells - removable_set
class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):
        # print("NEW INSTANCE")
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

    def find_neighbors(self, cell):
        neighbors = set()
        
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                
                # print(f"{i} --- {j}")
                if (i, j) == cell:
                    continue
                
                if i < self.height and j < self.width and i >= 0 and j >= 0:
                    if (i, j) not in self.moves_made:
                        neighbors.add((i, j))
        return neighbors
                
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
        self.moves_made.add(cell)
        self.safes.add(cell)
        self.mark_safe(cell)
        flag = False
        # print(f"I'm at {cell}")
        set_a = self.find_neighbors(cell)
        # set_a.add(cell)
        new_sentence = Sentence(set_a, count)
        
        # print(new_sentence)
        self.knowledge.append(new_sentence)

        index = self.knowledge.index(new_sentence)
        if new_sentence.known_mines() is not None:
            print(f"List is {len(self.knowledge)} long before 1a")
            for current_cell in new_sentence.known_mines():
                self.mark_mine(current_cell)
            try:
                self.knowledge.pop(index)
            except IndexError:
                print(f"1a) {index} is out of range when trying to remove {new_sentence} and list is {len(self.knowledge)} long")
            flag = True


        if new_sentence.known_safes() is not None: 
            print(f"List is {len(self.knowledge)} long before 1b")
            for current_cell in new_sentence.known_safes():
                self.mark_safe(current_cell)
            try:
                self.knowledge.pop(index)
            except IndexError:
                print(f"1b) {index} is out of range when trying to remove {new_sentence} and list is {len(self.knowledge)} long")
            flag = True

        removable_knowledge = []
        for curren_sentence in self.knowledge:
            if len(new_sentence.cells) != 0 and new_sentence.cells < curren_sentence.cells and curren_sentence not in removable_knowledge:
                print(f"\n----Found a subset for {new_sentence.cells} in {curren_sentence.cells} at {cell}\n---")
                inferred_sentence = Sentence(curren_sentence.cells - new_sentence.cells, curren_sentence.count - new_sentence.count)
                print(f"So, inferred a new sentence of {inferred_sentence}")
                self.knowledge.append(new_sentence)
                removable_knowledge.append(curren_sentence)
                flag = True
            elif len(new_sentence.cells) != 0 and new_sentence.cells > curren_sentence.cells  and new_sentence not in removable_knowledge: 
                print(f"\n----Found a superset for {new_sentence.cells} in {curren_sentence.cells} at {cell}\n---")
                inferred_sentence = Sentence(new_sentence.cells - curren_sentence.cells, new_sentence.count - new_sentence.count)
                print(f"So, inferred a new sentence of {inferred_sentence}")
                self.knowledge.append(inferred_sentence)
                removable_knowledge.append(new_sentence)
                flag = True
        
        for to_remove in removable_knowledge:
            self.knowledge.remove(to_remove)
        
        
        while flag:            
            flag = False
            for sentence in self.knowledge:
                index = self.knowledge.index(sentence) -1
                if sentence.known_mines() is not None:
                    print(f"List is {len(self.knowledge)} long before 2a")
                    for current_cell in sentence.known_mines():
                        self.mark_mine(current_cell)
                    try:
                        self.knowledge.pop(index)
                    except IndexError:
                        print(f"2a) {index} is out of range when trying to remove {sentence} and list is {len(self.knowledge)} long")
                        flag = True
                    
                if sentence.known_safes() is not None:
                    print(f"List is {len(self.knowledge)} long before 2b")    
                    for current_cell in sentence.known_safes():
                        self.mark_safe(current_cell)
                    try:
                        self.knowledge.pop(index)
                    except IndexError:
                        print(f"2b) {index} is out of range when trying to remove {sentence} and list is {len(self.knowledge)} long")
                    flag = True
            
            for i in range(len(self.knowledge)):
                for j in range(len(self.knowledge)):
                    if i == j:
                        continue
                    if len(new_sentence.cells) != 0 and self.knowledge[i].cells < self.knowledge[j].cells:
                        print(f"\n----Found a subset for {self.knowledge[i].cells} in {self.knowledge[j].cells}---\n")
                        new_sentence = Sentence(self.knowledge[j].cells - self.knowledge[i].cells, self.knowledge[j].count - self.knowledge[i].count)
                        self.knowledge.remove(self.knowledge[j])
                        self.knowledge.append(new_sentence) 
                        flag = True
                    if len(new_sentence.cells) != 0  and self.knowledge[i].cells > self.knowledge[j].cells:
                        print(f"\n----Found a superset for {self.knowledge[i].cells} in {self.knowledge[j].cells}---\n")
                        new_sentence = Sentence(self.knowledge[i].cells - self.knowledge[j].cells, self.knowledge[i].count - self.knowledge[j].count)
                        self.knowledge.remove( self.knowledge[i]) 
                        self.knowledge.append(new_sentence)
                        flag = True
                        
                        
    
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        print (len(self.safes))
        # if len(self.moves_made) == 0 or len(self.safes):
        #     return None
        
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell

        
        return None
    

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        while True:
            print("Hanging in here")
            i = random.randint(0, self.height - 1)
            j = random.randint(0, self.width - 1)
            if (i,j) not in self.moves_made or (i, j) not in self.mines:
                return (i,j)
        
        return NoneS