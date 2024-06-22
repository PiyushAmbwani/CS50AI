import sys
import itertools
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
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
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
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
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var, words in self.domains.items():
            remove_words = set()
            for word in words:
                if len(word) != var.length:
                    remove_words.add(word)
            self.domains[var] = words - remove_words
        # raise NotImplementedError

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlap = self.crossword.overlaps[x, y]
        if overlap is None:
            return False
        
        y_alphabet = set(each_wordy[overlap[1]] for each_wordy in self.domains[y])
        rm_wordsx = set(
            each_wordx for each_wordx in self.domains[x] if each_wordx[overlap[0]] not in y_alphabet)
        if len(rm_wordsx) > 0:
            self.domains[x] -= rm_wordsx
            return True
        # raise NotImplementedError

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        ## creating arcs for the domains universe##
        arcs_queue = arcs
        if arcs is None:
            arcs_queue = []
            for x, y in itertools.permutations(self.domains, 2):
                if y in self.crossword.neighbors(x):
                    arcs_queue.append((x, y))

        for arc in arcs_queue:
            x = self.revise(arc[0], arc[1])

        d_state = all(True if len(words) > 0 else False for _, words in self.domains.items())
        return d_state
        # raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        assign_check = False
        if assignment.keys() == self.crossword.variables: 
            return True
        return assign_check
        # raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        arc_check = True

        # Check assignment has all variables and have values
        flg = self.domains.keys() == assignment.keys()

        # Node consistency /  check uniary constraints, that is, value is correct length
        node_check = all(k.length == len(v) for k, v in assignment.items())

        # Arc consistency / check binary Constraints, that is, neighbors do not have conflicts
        for k, v in assignment.items():
            for neighbor in self.crossword.neighbors(k):
                (i, j) = self.crossword.overlaps[k, neighbor]
                if neighbor in assignment.keys() and (v[i] != assignment[neighbor][j] or v == assignment[neighbor]):
                    arc_check = arc_check and False

        return (node_check and arc_check)

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        if var in assignment.keys():
            return None
        neigbor_dict = {neighbor: self.domains[neighbor]
                        for neighbor in self.crossword.neighbors(var)}
        word_dict = {word: -1 for word in self.domains[var]}
        for word in word_dict.keys():
            for _, neighbor_values in neigbor_dict.items():
                if word in neighbor_values:
                    word_dict[word] += 1

        result = sorted(word_dict, key=word_dict.get)
        return result
        # raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        unassgn_var = self.crossword.variables - assignment.keys()
        dict_counter = {}
        dict_counter = {each: {"len_counter": len(self.domains[each]),
                               "degree": len(
                                   self.crossword.neighbors(each))} for each in unassgn_var}
        return_var = sorted(dict_counter, key=lambda x: (
            dict_counter[x]["len_counter"], dict_counter[x]["degree"]))
        return return_var[0]

        # raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result: 
                    return result
            del assignment[var]

        return None
        # raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
