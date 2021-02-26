grid = [[0, 2, 0, 6, 0, 8, 0, 0, 0],
        [5, 8, 0, 0, 0, 9, 7, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 0],
        [3, 7, 0, 0, 0, 0, 5, 0, 0],
        [6, 0, 0, 0, 0, 0, 0, 0, 4],
        [0, 0, 8, 0, 0, 0, 0, 1, 3],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 9, 8, 0, 0, 0, 3, 6],
        [0, 0, 0, 3, 0, 6, 0, 9, 0]
        ]
numbers = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

#this is some rudimentary code to solve a sudoku. As you can see the sudoku is a 2d List as shown above. 
#0s represent the empty cells. 
#I take a brute force method, i determine for every cell the possible numbers based on what numbers are already present.
# the next 3 functions do exactly that. they take the numbers that are there for every row, column and cell
# and make the geometric difference with the set "numbers" that is here above. the numbers that remain are the candidates

def numbers_from_row(row): #returns the possible numbers based on the row, so basically the missing numbers. 
    helper = []
    for i in grid[row]:
        helper.append(i)
    sett = set(helper)
    return (sett | numbers) - (sett & numbers)


def numbers_from_column(column): #returns the possible numbers based on the column, so basically the missing numbers. 
    helper = []
    for i in range(9):
        helper.append(grid[i][column])
    sett = set(helper)
    return (sett | numbers) - (sett & numbers)


def numbers_from_box(row, column):  #returns the possible numbers based in the cell, so basically the missing numbers. 
    helper = []
    if row % 3 == 2:
        row -= 2
    elif row % 3 == 1:
        row -= 1
    if column % 3 == 2:
        column -= 2
    elif column % 3 == 1:
        column -= 1
    for i in range(3):
        for l in range(3):
            helper.append(grid[row + i][column + l])
    sett = set(helper)
    return (sett | numbers) - (sett & numbers)


def possible_values(row, column): # this function just puts the 3 previous ones together, and determines for each cell the possible numbers
    if grid[row][column] != 0:
        return {grid[row][column]}
    for_row = numbers_from_row(row)
    for_column = numbers_from_column(column)
    for_box = numbers_from_box(row, column)
    return for_row & for_column & for_box


def possible_list(): # this function returns a 9 x 9 list, where in every cell, there is a list of possible numbers, based on the current grid
    empty = [[], [], [], [], [], [], [], [], []]
    for i in range(9):
        for l in range(9):
            empty[i].append([])
            if grid[i][l] == 0:
                empty[i][l] = list(possible_values(i, l))
            else:
                empty[i][l].append(grid[i][l])
    return empty


def solve(): #this function than actually solves the sudoku
    maybe = possible_list() #i initialize the first list with the "maybe" numbers, so for every cell, every number that could be there
    for row in range(9):
        for column in range(9): #i iterate over every cell
            possibleValues = maybe[row][column] #initialize the candidate numbers for the current cell
            if grid[row][column] != 0: #if the grid already has a number in this cell, just goes on to the next one
                continue
            if len(possibleValues) == 1: #if there is only one possible number, i put it in the grid and continue to the next cell
                grid[row][column] = possibleValues[0]
                maybe = possible_list() # and i update the maybe list, as there is a new number in the grid
                continue
            for possibleValue in possibleValues: # this is the case if there are multiple candidate numbers, which i iterate over
                grid[row][column] = possibleValue # i assigne to the cell in the grid the candidate number
                copymaybe = maybe # i make a copy of the current maybe list, because if the current number is not the right one, i have the backup
                maybe = possible_list() # i initialize the new maybe list based upon the grid with the candidate number
                if is_valid(maybe, row, column): # here i check if it is a valid number, the function is below
                    break
                else: # if it isnt a valid number, i reinitialize the cell to 0 and the maybe list to the old one
                    maybe = copymaybe
                    grid[row][column] = 0

    print(grid)

def is_valid(maybe, irow, icol):
    #here i extract for every cell, all the numbers in its row, cell and box, in the maybe list.
    # and look if all the numbers are present. Because if i have a candidate numbewr, which excludes from the maybe list 
    # numbers, so that in that row, a certain number cannot appear anymore, its of course not a valid candidate.
    #and i also check if there are empty lists in the maybe list, because then also the maybe list is not valid
    #and consequently the number i am staging.
    length_checker = True
    for row in range(irow, 9): # here i iterate over every cell thats after the one ia am currently trying to solve
        for col in range(icol, 9):
            rows, column, box = [], [], []  
            for l in maybe[row]: 
                rows.extend(l)
            for s in range(9):
                column.extend(maybe[s][col])
            copycol, copyrow = col, row
            if row % 3 == 2:
                row -= 2
            elif row % 3 == 1:
                row -= 1
            if col % 3 == 2:
                col -= 2
            elif col % 3 == 1:
                col -= 1
            for i in range(3):
                for l in range(3):
                    box.extend(maybe[row + i][col + l])
            number_checker = ((numbers - set(rows) == {0}) and (numbers - set(column) == {0}) and (numbers - set(box) == {0}))
            col, row = copycol, copyrow
            if not number_checker:
                return False
            else:
                continue
    for l in maybe: 
        for s in l:
            if len(s) == 0:
                length_checker = False
    if length_checker:
        return True
    else:
        return False

solve()
