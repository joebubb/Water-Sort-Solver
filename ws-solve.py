from enum import Enum

# these are all of the colors in the game 
ALLOWED_COLORS = ["red", "orange", "green", "light-green", "periwinkle", 
                  "indigo", "purple", "pink", "gray"]

class Color(Enum): 
    Red = "red"
    Orange = "orange"
    Green = "green"
    LightGreen = "light-green"
    Periwinkle = "periwinkle"
    Indigo = "indigo"
    Purple = "purple"
    Pink = "pink"
    Gray = "gray"


class Game: 
    def __init__(self):
        self.tubes = [] 
        self.move_history = []

    def _copy(self): 
        game = Game() 
        game.tubes = self.tubes.copy()
        game.move_history = self.move_history.copy()
        return game

    def _count_all_colors(self): 
        d = {}
        for tube in self.tubes: 
            for color in tube: 
                if color in d: 
                    d[color] += 1
                else: 
                    d[color] = 1
        return d 

    def _all_possible_moves(self): 
        moves = []
        for src in range(len(self.tubes)): 
            for dest in range(len(self.tubes)): 
                if src != dest: 
                    # if source tube is empty then move isn't possible 
                    if len(self.tubes[src]) == 0: 
                        pass 
                    # same for if the destination tube is full
                    elif len(self.tubes[dest]) == 4: 
                        pass 
                    # else check if the top colors match 
                    # or if dest is empty
                    else: 
                        if len(self.tubes[dest]) == 0: 
                            moves += [(src, dest)]
                        elif self.tubes[src][-1] is self.tubes[dest][-1]: 
                            moves += [(src, dest)]
        return moves

    def _make_move(self, src, dest): 
        # update the move history
        self.move_history.append((src, dest))
        src_tube = self.tubes[src]
        dest_tube = self.tubes[dest]
        # transfer the top color until it is no longer possible
        while len(src_tube) > 0: 
            # if dest is empty we can transfer
            if len(dest_tube) == 0: 
                dest_tube.append(src_tube.pop())
            # if the colors match we can transfer
            elif src_tube[-1] is dest_tube[-1]: 
                dest_tube.append(src_tube.pop())
            # else break early because tranfering would break the rules
            else: 
                break

    def is_solvable(self): 
        d = self._count_all_colors() 
        for color, count in d.items(): 
            # if a color appears and it hasn't appeared exactly 4 times, 
            # the game is un-solvable
            if count != 4: 
                return False 
        return True 

    def is_solved(self): 
        """
            Returns a boolean value representing whether the game is 
            in a solved state or not. 
        """
        for tube in self.tubes: 
            if len(tube) == 0: 
                continue
            else:
                first_color = tube[0]
                for color in tube: 
                    if not (color is first_color): 
                        return False
                if len(tube) != 4: 
                    return False 
        return True 

    def attempt_to_solve(self): 
        """
            Uses a recursive backtracking algorithm to attempt to
            solve the game. 
        """
        if self.is_solved(): 
            return self._copy()
        elif not self.is_solvable(): 
            return 
        else: 
            # for every possible move, make a move on a copy of this game 
            # then, if it is solved, return 
            # else, continue the loop 
            for move in self._all_possible_moves(): 
                cpy = self._copy() 
                cpy._make_move(move[0], move[1])
                if cpy.is_solved(): 
                    return cpy 
                else: 
                    res = cpy.attempt_to_solve() 
                    if res is None: 
                        continue
                    else: 
                        return res


def get_number_of_tubes(): 
    """
        Prompts the user for the number of tubes until an integer is given.
    """
    number_of_tubes = input("How many tubes are there: ")
    while True: 
        # keep getting input until an int is given
        try: 
            return int(number_of_tubes)
        except: 
            print("You must type an integer.")
            number_of_tubes = input("How many tubes are there: ")


def all_colors_valid(colors): 
    """
        Returns a boolean value representing whether or not every color 
        entered by the user is in the game.
    """
    # attempts to make a Color object for each color 
    for color in colors: 
        try: 
            Color(color)
        except ValueError: 
            # if this fails then no color in the enum matches the string 
            return False 
    return True 


def color_counts_valid(tubes): 
    """
        Makes sure that there is not more than 4 of each color.
    """
    counts = {} 
    for tube in tubes: 
        for color in tube: 
            if color in counts: 
                counts[color] += 1
            else: 
                counts[color] = 1 
    for color, count in counts.items(): 
    # returns a tuple with the validity of the colors 
    # as well as the offending color if there is one 
        if count > 4: 
            return False, color
    return True, None 


def fill_tubes(game, n): 
    """
        Prompts the user to fill any number of tubes, 
        then adds the tubes to the game.
    """
    # show the user the rules 
    print()
    print("Enter the contents of each tube. Separate each color by spaces.")
    print("The following colors are allowed: " + " ".join(ALLOWED_COLORS))
    print("You can type nothing to indicate that the tube is empty.")
    print()
    # fill each tube 
    tubes_filled = 0 
    while tubes_filled < n: 
        print(f"Tube #{tubes_filled+1}")
        colors = input("Enter the colors: ").lower().split()
        # check validity of colors 
        if not all_colors_valid(colors): 
            print("An invalid color was entered.")
            print("Try double checking your spelling.")
            print()
            continue

        colors = [Color(c) for c in colors]
        # check number of colors (there cannot be more than 4 of each color)
        valid, offending_color = color_counts_valid(game.tubes + [colors])
        if not valid: 
            print(f"The following color has appeared more than 4 times: \
                {offending_color.value}")
            print()
            continue

        # if everything is ok, add this tube to the game 
        game.tubes += [colors]
        tubes_filled += 1


def get_filename(): 
    filename = input("Choose a name for the file: ")
    while not filename: 
        print("The file name cannot be an empty string.")
        filename = input("Choose a name for the file: ")
    return filename

        
if __name__ == "__main__": 
    # get number of tubes 
    number_of_tubes = get_number_of_tubes() 

    # set up Game object 
    game = Game() 
    fill_tubes(game, number_of_tubes)
    
    # solve 
    res = game.attempt_to_solve()

    # write the solution to a file if there is a solution 
    if not (res is None): 
        print("A solution has been found!")
        filename = get_filename()
        with open(filename, 'w') as f: 
            for move in res.move_history: 
                f.write(f"Pour tube {move[0]+1} into tube {move[1]+1}.\n")
            f.write("Solved!")
    else: 
        print("No solution has been found.")