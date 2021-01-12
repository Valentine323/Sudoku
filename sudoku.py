# -*- coding: utf-8 -*-
# """
# Created on Thu Nov 19 09:55:14 2020
# SUDOKU
# @author: csokizoli
#
#
# """
#HIBA A 198. soron

## INCLUDES
import numpy as np


## CLASSES AND FUNCTIONS

class pole:#class in which all the data about the sudoku cell is stored - values, candidates
    def __init__(self, value):
        self.Value = value
        if self.Value == 0:#if the input field is empty
            self.Value = None
            self.Candids = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9], dtype=np.uint8)
        else:
            self.Candids = np.empty((0,), dtype=np.uint8)

    def set(self,value):#sets the value and removes all candidates
        self.Value = value
        self.Candids = np.empty((0,), dtype=np.uint8)#easier that way than removing the candids

    def is_trivial(self):#if the cell has only one candidate returns true
        return True if len(self.Candids) == 1 else False

    def remove(self, candid):#removes desired candidates
        if isinstance(candid, np.ndarray):#multiple
            for i in range(len(candid)):
                self.Candids = np.delete(self.Candids, self.Candids == candid[i])
        else:#single
            self.Candids = np.delete(self.Candids, self.Candids == candid)

    def remove_exc(self, candid):#removes all candids except the one(s) given to the method (often needed)
        if isinstance(candid, np.ndarray):#multiple
            for i in range(0, len(candid)):
                self.Candids = np.delete(self.Candids, self.Candids != candid[i])
        else:#single
            self.Candids = np.delete(self.Candids, np.where(self.Candids != candid))

def puzzle_is_solved(puzzle):#checks whether the puzzle is solved
    for r in range(9):
        for c in range(9):
            if puzzle[r][c].Value == 0 or len(puzzle[r][c].Candids) > 0:
                return False#if some cell is blank (length condition is for safety reasons:
                # should it happen that the value is set, but there are candids - setting value by puzzle.Value= IS NOT RECOMMENDED)
    return True

def hidden_single(puzzle, position, dim):#algoritm for hidden single (see: https://www.algoritmy.net/article/1351/Sudoku)
    r, c = (position)#position of the current element
    if not puzzle[r][c].is_trivial():# if it has more than one candidates
        #CHECKING THE CONDITIONS FOR 'HIDDEN SINGLE'
        # in row
        if dim == 'r' or dim == 'row':
            for i in range(9):
                intersect = np.intersect1d(puzzle[r][c].Candids, puzzle[r][i].Candids)#intersection of candidates
                union = np.union1d(puzzle[r][c].Candids, puzzle[r][i].Candids)#union of candidates
                #if union has +1 element, it means, that we have found a hidden single
                # other conditions for safety reasons: the intersection cant be empty, the examined cell must have that one candidate more, in order for this function to work properly
                if len(union) == (len(intersect) + 1) and len(intersect) > 0 and len(puzzle[r][c].Candids) > len(puzzle[r][i].Candids):
                    # print(puzzle[r][c].Candids)
                    # print(puzzle[r][i].Candids)
                    try:
                        numbers
                        if np.all(numbers == intersect):#if same numbers were found
                            coords = np.vstack((coords, [r, i]))#add the coordinates to the matrix of coordinates
                    except NameError:#if the numbers value does not yes exist, create it and store the common numbers + the matrix to save the coordinates
                        coords = np.empty((0, 2), dtype=np.uint8)
                        numbers = intersect
            try:
                coords
                if coords.shape[0] == (len(puzzle[r][c].Candids) - 1):#if we have one less cell than candidates of the examined (given to the function);
                    # for i in range(np.shape(coords)[0] - 1):#IT IS ALL WRONG, By commenting this out the solver works better - I don't know what was I thinking
                    #     puzzle[coords[i][0]][coords[i][1]].remove_exc(numbers)
                    # print(coords)
                    puzzle[r][c].remove(numbers)#remove the common numbers
                    puzzle[r][c].set(puzzle[r][c].Candids[0])#set the value of the cell
            except NameError:
                pass#if there was no other cells suffising the conditions above, do nothing

        # in column
        if dim == 'c' or dim == 'col':
            for i in range(9):
                intersect = np.intersect1d(puzzle[r][c].Candids, puzzle[i][c].Candids)
                union = np.union1d(puzzle[r][c].Candids, puzzle[i][c].Candids)
                if len(union) == (len(intersect) + 1) and len(intersect) > 0 and len(puzzle[r][c].Candids) > len(puzzle[i][c].Candids):
                    # print(puzzle[r][c].Candids)
                    # print(puzzle[i][c].Candids)
                    try:
                        numbers
                        if np.all(numbers == intersect):
                            coords = np.vstack((coords, [i, c]))
                    except NameError:
                        coords = np.empty((0, 2), dtype=np.uint8)
                        numbers = intersect
            try:
                coords
                if coords.shape[0] == (len(puzzle[r][c].Candids) - 1):
                    # for i in range(np.shape(coords)[0] - 1):
                    #     puzzle[coords[i][0]][coords[i][1]].remove_exc(numbers)
                    # print(coords)
                    puzzle[r][c].remove(numbers)
                    # puzzle[r][c].Value = puzzle[r][c].Candids[0]
                    # puzzle[r][c].remove(puzzle[r][c].Value)
                    puzzle[r][c].set(puzzle[r][c].Candids[0])
            except NameError:
                pass

        # in region
        if dim == 's' or dim == 'square':
            # determine in which group the given cell is in
            square_r = r // 3
            square_c = c // 3
            for i in range(3):
                for j in range(3):
                    intersect = np.intersect1d(puzzle[r][c].Candids, puzzle[3 * square_r + i][3 * square_c + j].Candids)
                    union = np.union1d(puzzle[r][c].Candids, puzzle[3 * square_r + i][3 * square_c + j].Candids)
                    if len(union) == (len(intersect) + 1) and len(intersect) > 0 and len(puzzle[r][c].Candids) > len(puzzle[3 * square_r + i][3 * square_c + j].Candids):
                        # print(str([3 * square_r + i])+'x'+str([3 * square_c + j]))
                        # print(puzzle[r][c].Candids)
                        # print(puzzle[3 * square_r + i][3 * square_c + j].Candids)
                        try:
                            numbers
                            if np.all(numbers == intersect):
                                coords = np.vstack((coords, [3 * square_r + i, 3 * square_c + j]))
                        except NameError:
                            coords = np.empty((0, 2), dtype=np.uint8)
                            numbers = intersect
            try:
                coords
                if coords.shape[0] == (len(puzzle[r][c].Candids) - 1):
                    # for i in range(np.shape(coords)[0] - 1):
                    #     puzzle[coords[i][0]][coords[i][1]].remove_exc(numbers)
                    # print(coords)
                    puzzle[r][c].remove(numbers)
                    # puzzle[r][c].Value = puzzle[r][c].Candids[0]
                    # puzzle[r][c].remove(puzzle[r][c].Value)
                    puzzle[r][c].set(puzzle[r][c].Candids[0])
            except NameError:
                pass
    else:#if the cell is trivial, set its value
        puzzle[r][c].set(puzzle[r][c].Candids[0])

def purge_candids(puzzle):    # Purging candidates
    # remove the value of the cell from the candidates of other cells, which accoding to the sudoku's rules cant be candidate for those cells
    for r in range(9):
        for c in range(9):
            if puzzle[r][c].Value is not None:
                for i in range(9):
                    # print('From {} row {} column deleted {}'.format(i, c, puzzle[r][c].Value),end='')
                    # print(' From {} row {} column deleted {}'.format(r, i, puzzle[r][c].Value),end='')
                    puzzle[i][c].remove(puzzle[r][c].Value)#from row
                    puzzle[r][i].remove(puzzle[r][c].Value)#from column
                    # print('\n')
                #from group
                squares_r = r // 3
                squares_c = c // 3
                for i in range(3):
                    for j in range(3):
                        puzzle[3 * squares_r + i][3 * squares_c + j].remove(puzzle[r][c].Value)
                        # print('From {} row {} column deleted {}\n'.format(3 * squares_r + i, 3 * squares_c + j, puzzle[r][c].Value))

def set_trivials(puzzle):#the work of this function may be redundant by introducing the hidden_single function
    for r in range(9):
        for c in range(9):
            if puzzle[r][c].is_trivial():
                puzzle[r][c].set(puzzle[r][c].Candids[0])

def naked_pair(puzzle, coordinates):#algoritm for naked pairs (see: https://www.algoritmy.net/article/1351/Sudoku)
    r, c= coordinates#parse coordinates of the given position
    if (not puzzle[r][c].is_trivial() and len(puzzle[r][c].Candids)):
        # determine in which group the given cell is in
        square_r = coordinates[0] // 3
        square_c = coordinates[1] // 3
        for i in range(3):
            for j in range(3):
                #if the two,three,four... cells have the same candidades
                if np.array_equal(puzzle[r][c].Candids, puzzle[3 * square_r + i, 3 * square_c + j].Candids):
                    try:
                        coords
                        coords = np.vstack((coords, [3 * square_r + i, 3 * square_c + j]))
                    except NameError:
                        coords = np.empty((0, 2), dtype=np.uint8)
                        coords = np.vstack((coords, [3 * square_r + i, 3 * square_c + j]))
        try:
            coords#if there were cells with same candidates found
            #if there is as many cells with the same candidates as there are candidates (2 same candidates in 2 cells in 1 group, 3same candidates in 3 cells... etc.)
            if coords.shape[0] == len(puzzle[r][c].Candids):
                for i in range(3):
                    for j in range(3):
                        if not ((coords == [3 * square_r + i, 3 * square_c + j]).all(axis=1)).any() and len(puzzle[3 * square_r + i][3 * square_c + j].Candids)>0:#if cell is not one of those, which contain the candidates
                            # print('From position [{}][{}]  Deleted candids:{}'.format(3 * square_r + i, 3 * square_c + j, puzzle[r][c].Candids))
                            puzzle[3 * square_r + i][3 * square_c + j].remove(puzzle[r][c].Candids)#remove candidates
        except NameError:
            pass
    else:  # if the cell is trivial, set its value  ----- IF AN ERROR OCCURES IN THE FUTURE - CHECK THIS
        # print('row:{} col:{}'.format(r,c))
        if np.isnan(puzzle[r][c].Value):
            puzzle[r][c].set(puzzle[r][c].Candids[0])

## MAIN BODY

## PREPARATION STEPS
# reading in the file
f = open('sudoku3.txt', 'r')
s = open('solution3.txt','r')
# removing separators
sequence_in = f.read().replace('\n', '').replace(' ', '').replace(',', '').replace(';', '')
f.close()
sequence_sol = s.read().replace('\n', '').replace(' ', '').replace(',', '').replace(';', '')
s.close()
length = len(sequence_in)

# check number of elements
if length != 81 & length != sequence_in.isdigit():
    print('Input is not in the right format or length')
vstup = np.array([s for s in sequence_in], dtype=np.uint8)
reseni = np.array([s for s in sequence_sol], dtype=np.uint8)
np.ndarray.resize(vstup, (9, 9))
np.ndarray.resize(reseni, (9, 9))

# create an array of classes
puzzle = np.ndarray((9, 9), dtype=np.dtype(pole))
# copying stuff to the array of classes
for i in range(9):
    for j in range(9):
        puzzle[i][j] = pole(vstup[i][j])

## SOLVING STEPS


counter = 1
while not puzzle_is_solved(puzzle) and counter < 20:

    # Purging candidates
    purge_candids(puzzle)

    # Filling singles
    #theoretically it could go in the for cycles above with an elif
    for r in range(9):
        for c in range(9):
            if puzzle[r][c].is_trivial():
                puzzle[r][c].set(puzzle[r][c].Candids[0])

    # for r in range(9):
    #     for c in range(9):
    #         print(str([r,c])+':'+str(puzzle[r][c].Candids)+'\n')


    # Filling hidden singles
    # puzzle_cpy = np.copy(puzzle)
    for r in range(9):
        for c in range(9):
            # print(str(r) + 'x' + str(c) + '\n')
            hidden_single(puzzle, (r, c), 'r')
            hidden_single(puzzle, (r, c), 'c')
            hidden_single(puzzle, (r, c), 's')


    # Naked pairs
    for i in range(9):
        for j in range(9):
            naked_pair(puzzle, (i, j))

    counter += 1

# printing result
# print(puzzle_is_solved(puzzle))
print('vstup\n')
print(vstup)
print('\n')

vystup = np.ndarray((9, 9), dtype=np.dtype('uint8'))
for i in range(9):
    for j in range(9):
        if puzzle[i][j].Value is not None:
            vystup[i][j] = puzzle[i][j].Value
        else:
            vystup[i][j] = 0

print('vystup\n')
print(vystup)
print('\n')

print('reseni\n')
print(reseni)
print('\n')

#PRINTING ALL CANDIDS TO SEE BETTER
print('CANDIDS\n')
for i in range(9):
    for j in range(9):
        c=len(puzzle[i][j].Candids)
        if c:
            for k in range(9):
                if c-k > 0:
                    print(puzzle[i][j].Candids[k], end='')
                else:
                    print('_', end='')
            print('\t', end='')
        else:
            print(str(puzzle[i][j].Value)+'!______\t', end='')
    print('\n')