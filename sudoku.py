# -*- coding: utf-8 -*-
# """
# Created on Thu Nov 19 09:55:14 2020
# SUDOKU
# @author: csokizoli
#
#
# """

## INCLUDES
import numpy as np

## CLASSES AND FUNCTIONS

class pole:#class in which all the data about the sudoku cell is stored - values, candidates
    def __init__(self, value):
        if value == 0:#if the input field is empty
            self.Candids = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9], dtype=np.uint8)
        else:
            self.Candids = np.array([value], dtype=np.uint8)

    def set(self,value):#sets the value and removes all candidates
        self.Candids = np.array([value], dtype=np.uint8)

    def is_trivial(self):#if the cell has only one candidate returns true
        return True if len(self.Candids) == 1 else False

    def remove(self, candid):#removes desired candidates
        if isinstance(candid, np.ndarray) and (len(self.Candids)-len(candid))>0:
            for i in range(len(candid)):
                self.Candids = np.delete(self.Candids, self.Candids == candid[i])

    def remove_exc(self, candid):#removes all candids except the one(s) given to the method (often needed)
        if isinstance(candid, np.ndarray):
            for i in range(len(candid)):
                self.Candids = np.delete(self.Candids, self.Candids != candid[i])

def puzzle_is_solved(puzzle):#checks whether the puzzle is solved
    for r in range(9):
        for c in range(9):
            if len(puzzle[r,c].Candids) > 1:
                return False#if some cell is blank
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
                    puzzle[r][c].remove(numbers)
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
                    puzzle[r][c].remove(numbers)
                    puzzle[r][c].set(puzzle[r][c].Candids[0])
            except NameError:
                pass

def purge_candids(puzzle):    # Purging candidates
    # remove the value of the cell from the candidates of other cells, which accoding to the sudoku's rules cant be candidate for those cells
    for r in range(9):
        for c in range(9):
            if len(puzzle[r][c].Candids)==1:
                for i in range(9):
                    puzzle[i][c].remove(puzzle[r][c].Candids)#from row
                    puzzle[r][i].remove(puzzle[r][c].Candids)#from column
                #from group
                squares_r = r // 3
                squares_c = c // 3
                for i in range(3):
                    for j in range(3):
                        puzzle[3 * squares_r + i][3 * squares_c + j].remove(puzzle[r][c].Candids)

def set_trivials(puzzle):#the work of this function may be redundant by introducing the hidden_single function
    for r in range(9):
        for c in range(9):
            if puzzle[r][c].is_trivial():
                puzzle[r][c].set(puzzle[r][c].Candids[0])

def naked_pair(puzzle, coordinates):#algoritm for naked pairs (see: https://www.algoritmy.net/article/1351/Sudoku)
    r, c= coordinates#parse coordinates of the given position
    if len(puzzle[r][c].Candids)>1:
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
    # else:  # if the cell is trivial, set its value  ----- IF AN ERROR OCCURES IN THE FUTURE - CHECK THIS
    #     if np.isnan(puzzle[r][c].Value):
    #         puzzle[r][c].set(puzzle[r][c].Candids[0])

def pointing_pairs(puzzle, scoordinates):
    r, c = scoordinates #getting the position of the group (larger squares)
    #cols
    #getting the intersection of candids in each column
    ic1 = np.intersect1d(np.intersect1d(puzzle[3 * r][3 * c].Candids, puzzle[3 * r + 1][3 * c].Candids, True), puzzle[3 * r + 2][3 * c].Candids, True)
    ic2 = np.intersect1d(np.intersect1d(puzzle[3 * r][3 * c + 1].Candids, puzzle[3 * r + 1][3 * c + 1].Candids, True), puzzle[3 * r + 2][3 * c + 1].Candids, True)
    ic3 = np.intersect1d(np.intersect1d(puzzle[3 * r][3 * c + 2].Candids, puzzle[3 * r + 1][3 * c + 2].Candids, True), puzzle[3 * r + 2][3 * c + 2].Candids, True)
    #getting the union of candids in each column
    uc1 = np.union1d(np.union1d(puzzle[3 * r][3 * c].Candids, puzzle[3 * r + 1][3 * c].Candids), puzzle[3 * r + 2][3 * c].Candids)
    uc2 = np.union1d(np.union1d(puzzle[3 * r][3 * c + 1].Candids, puzzle[3 * r + 1][3 * c + 1].Candids), puzzle[3 * r + 2][3 * c + 1].Candids)
    uc3 = np.union1d(np.union1d(puzzle[3 * r][3 * c + 2].Candids, puzzle[3 * r + 1][3 * c + 2].Candids), puzzle[3 * r + 2][3 * c + 2].Candids)
    #getting the union of each combination of pairs of unions
    uc12 = np.union1d(uc1, uc2)
    uc23 = np.union1d(uc2, uc3)
    uc31 = np.union1d(uc3, uc1)

    #rows
    #getting the intersection of candids in each row
    ir1 = np.intersect1d(np.intersect1d(puzzle[3 * r][3 * c].Candids, puzzle[3 * r][3 * c + 1].Candids, True), puzzle[3 * r][3 * c + 2].Candids, True)
    ir2 = np.intersect1d(np.intersect1d(puzzle[3 * r + 1][3 * c].Candids, puzzle[3 * r + 1][3 * c + 1].Candids, True), puzzle[3 * r + 1][3 * c + 2].Candids, True)
    ir3 = np.intersect1d(np.intersect1d(puzzle[3 * r + 2][3 * c].Candids, puzzle[3 * r + 2][3 * c + 1].Candids, True), puzzle[3 * r + 2][3 * c + 2].Candids, True)
    #getting the union of candids in each row
    ur1 = np.union1d(np.union1d(puzzle[3 * r][3 * c].Candids, puzzle[3 * r][3 * c + 1].Candids),puzzle[3 * r][3 * c + 2].Candids)
    ur2 = np.union1d(np.union1d(puzzle[3 * r + 1][3 * c].Candids, puzzle[3 * r + 1][3 * c + 1].Candids),puzzle[3 * r + 1][3 * c + 2].Candids)
    ur3 = np.union1d(np.union1d(puzzle[3 * r + 2][3 * c].Candids, puzzle[3 * r + 2][3 * c + 1].Candids),puzzle[3 * r + 2][3 * c + 2].Candids)
    #getting the union of each combination of pairs of unions
    ur12 = np.union1d(ur1, ur2)
    ur23 = np.union1d(ur2, ur3)
    ur31 = np.union1d(ur3, ur1)

    #if at least one of the column-intersections is not an empty set
    if (ic1.size > 0) | (ic1.size > 0) | (ic3.size > 0):
        #if the first column has unique elements
        if np.intersect1d(ic1, uc23).size == 0 and ic1.size > 0:
            subcol=0
            col_unique=ic1
        #if the second column has unique elements
        if np.intersect1d(ic2, uc31).size == 0 and ic2.size > 0:
            subcol=1
            col_unique=ic2
        #if the third column has unique elements
        if np.intersect1d(ic3, uc12).size == 0 and ic3.size > 0:
            subcol=2
            col_unique=ic3
        try:
            #if one of the ifes above was triggered
            col_unique
            #go trough the column and remove the candids from other rows
            for i in range(9):
                if i<3*r or i>3*r+2:#leave out the rows in which the pointing pairs were detected
                    puzzle[i][3*c+subcol].remove(col_unique)
            del col_unique
        except NameError:#if none of the ifs above were triggered, continue
            pass

    #if at least one of the row-intersections is not an empty set
    if (ir1.size > 0) | (ir2.size > 0) | (ir3.size > 0):
        #if the first row has unique elements
        if np.intersect1d(ir1, ur23).size == 0 and ir1.size > 0:
            subrow=0
            row_unique=ir1
        #if the second row has unique elements
        if np.intersect1d(ir2, ur31).size == 0 and ir2.size > 0:
            subrow=1
            row_unique=ir2
        #if the third row has unique elements
        if np.intersect1d(ir3, ur12).size == 0 and ir3.size > 0:
            subrow=2
            row_unique=ir3
        try:
            # if one of the ifes above was triggered
            row_unique
            # go trough the row and remove the candids from other columns
            for i in range(9):
                if i<3*c or i>3*c+2:#leave out the columns in which the pointing pairs were detected
                    puzzle[r+subrow][i].remove(row_unique)
            del row_unique
        except NameError:#if none of the ifs above were triggered, continue
            pass

def box_line_reduction(puzzle, position, row_or_col):
    #rows
    if row_or_col == 'r':
        #get the union of candidates for all 3 groups in the intersection with the given row
        first=np.union1d(np.union1d(puzzle[position][0].Candids, puzzle[position][1].Candids), puzzle[position][2].Candids)
        second=np.union1d(np.union1d(puzzle[position][3].Candids, puzzle[position][4].Candids), puzzle[position][5].Candids)
        third=np.union1d(np.union1d(puzzle[position][6].Candids, puzzle[position][7].Candids), puzzle[position][8].Candids)
        #get the index of the group (0,1,2) trough which the given row passes trough
        sq_row = position // 3
    #columns
    if row_or_col == 'c':
        # get the union of candidates for all 3 groups in the intersection with the given column
        first=np.union1d(np.union1d(puzzle[0][position].Candids, puzzle[1][position].Candids), puzzle[2][position].Candids)
        second=np.union1d(np.union1d(puzzle[3][position].Candids, puzzle[4][position].Candids), puzzle[5][position].Candids)
        third=np.union1d(np.union1d(puzzle[6][position].Candids, puzzle[7][position].Candids), puzzle[8][position].Candids)
        # get the index of the group (0,1,2) trough which the given column passes trough
        sq_col = position // 3

    #Get the unions of candidates of each combination of the 3 groups
    u23 = np.union1d(second, third)
    u31 = np.union1d(first, third)
    u12 = np.union1d(first, second)
    #Get the candidates which are exclusive for the given group
    first_exclusive = np.setdiff1d(first, u23, True)
    second_exclusive = np.setdiff1d(second, u31, True)
    third_exclusive = np.setdiff1d(third, u12, True)

    #if the first group has unique candidates
    if (first_exclusive.size > 0):
        #iterate trough that group
        for i in range(3):
            for j in range(3):
                #if row
                if row_or_col == 'r':
                    if position!=3*sq_row+i:#if the position is not in first row of the group
                        puzzle[3*sq_row+i,j].remove(first_exclusive)#remove the candidates
                        # if puzzle[3*sq_row+i,j].Candids.size==0:
                        #     print([3*sq_row+i,j],end=' ')
                        #     print('vynulovano first R')
                #if column
                if row_or_col == 'c':
                    if position!=3*sq_col+j:#if the position is not in first column of the group
                        puzzle[i,3*sq_col+j].remove(first_exclusive)#remove the candidates
                        # if puzzle[i,3*sq_col+j].Candids.size==0:
                        #     print([i,3*sq_col+j],end=' ')
                        #     print('vynulovano first C')
    if (second_exclusive.size > 0):
        for i in range(3):
            for j in range(3):
                if row_or_col == 'r':
                    if position != 3*sq_row+i:#if the position is not in second row of the group
                        puzzle[3 * sq_row + i,3+j].remove(second_exclusive)#remove the candidates
                        # if puzzle[3 * sq_row + i,3+j].Candids.size==0:
                        #     print([3 * sq_row + i,3+j],end=' ')
                        #     print('vynulovano second R')
                if row_or_col == 'c':
                    if position != 3*sq_col+j:#if the position is not in second column of the group
                        puzzle[3+i,3 * sq_col + j].remove(second_exclusive)#remove the candidates
                        # if puzzle[3+i,3 * sq_col + j].Candids.size==0:
                        #     print([3+i,3 * sq_col + j],end=' ')
                        #     print('vynulovano second C')
    if (third_exclusive.size > 0):
        for i in range(3):
            for j in range(3):
                if row_or_col == 'r':
                    if position != 3*sq_row+i:#if the position is not in third row of the group
                        puzzle[3 * sq_row + i,6+j].remove(third_exclusive)#remove the candidates
                        # if puzzle[3 * sq_row + i,6+j].Candids.size==0:
                        #     print([3 * sq_row + i,6+j],end=' ')
                        #     print('vynulovano third R')
                if row_or_col == 'c':
                    if position != 3*sq_col+j:#if the position is not in third column of the group
                        puzzle[6+i,3 * sq_col + j].remove(third_exclusive)#remove the candidates
                        # if puzzle[6+i,3 * sq_col + j].Candids.size==0:
                        #     print([6+i,3 * sq_col + j],end=' ')
                        #     print('vynulovano third C')




####################################################################################################
####################################################################################################
#################################### MAIN BODY #####################################################
####################################################################################################
####################################################################################################
## PREPARATION STEPS
# reading in the file
f = open('sudoku2.txt', 'r')
s = open('solution2.txt','r')
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
    # for r in range(9):
    #     for c in range(9):
    #         if puzzle[r][c].is_trivial():
    #             puzzle[r][c].set(puzzle[r][c].Candids[0])

    # for r in range(9):
    #     for c in range(9):
    #         print(str([r,c])+':'+str(puzzle[r][c].Candids)+'\n')


    # Filling hidden singles
    # for r in range(9):
    #     for c in range(9):
    #         # print(str(r) + 'x' + str(c) + '\n')
    #         hidden_single(puzzle, (r, c), 'r')
    #         hidden_single(puzzle, (r, c), 'c')
    #         hidden_single(puzzle, (r, c), 's')


    # Naked pairs
    # for i in range(9):
    #     for j in range(9):
    #         naked_pair(puzzle, (i, j))



    # Pointing pairs
    for i in range(3):
        for j in range(3):
            pointing_pairs(puzzle, [i,j])

    #Box_line_reduction
    # for i in range(9):
    #         box_line_reduction(puzzle,i,'r')
    #         box_line_reduction(puzzle,i,'c')

    print('CANDIDS\n')
    for i in range(9):
        for j in range(9):
            if len(puzzle[i][j].Candids) > 1:
                for k in range(9):
                    if len(puzzle[i][j].Candids) - k > 0:
                        print(puzzle[i][j].Candids[k], end='')
                    else:
                        print('_', end='')
                print('\t', end='')
            else:
                print(str(puzzle[i][j].Candids[0]) + '!______\t', end='')
        print('\n')


    if puzzle_is_solved(puzzle):
        print(counter)
        break
    counter += 1

# printing result
# print(puzzle_is_solved(puzzle))
print('vstup\n')
print(vstup)
print('\n')

vystup = np.ndarray((9, 9), dtype=np.dtype('uint8'))
for i in range(9):
    for j in range(9):
        if len(puzzle[i][j].Candids)==1:
            vystup[i][j] = puzzle[i][j].Candids[0]
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
        if len(puzzle[i][j].Candids) >1:
            for k in range(9):
                if len(puzzle[i][j].Candids)-k > 0:
                    print(puzzle[i][j].Candids[k], end='')
                else:
                    print('_', end='')
            print('\t', end='')
        else:
            print(str(puzzle[i][j].Candids[0])+'!______\t', end='')
    print('\n')

print('Puzzle solved successfully' if (reseni-vystup==0).all() else 'Puzzle has not been solved')