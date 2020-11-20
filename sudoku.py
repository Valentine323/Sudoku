# -*- coding: utf-8 -*-
#"""
#Created on Thu Nov 19 09:55:14 2020
#SUDOKU
#@author: csokizoli
#
#
#
#
#ISSUES TO SOLVE:
#-Last element after using the section "finding singletons" is always 9, no matter what
#-That same part of the code doesnt seem to work at all-debugging needed
#
#"""


## INCLUDES
import numpy as np



## CLASSES AND FUNCTIONS
class pole:
    def __init__(self,value):
        self.Value=value
        if self.Value==0:
            self.Candids=np.array([1, 2, 3, 4, 5, 6, 7, 8, 9],dtype=np.uint8)
        else:
            self.Candids=np.empty((0,),dtype=np.uint8)
    def is_trivial(self):
        return True if len(self.Candids)==1 else False
    def remove(self,candid):
        if isinstance(candid, np.ndarray):
            for i in range(0, len(candid)): 
                self.Candids=np.delete(self.Candids,self.Candids==candid[i])
        else:
            self.Candids=np.delete(self.Candids,self.Candids==candid)
    def remove_exc(self,candid):
        self.Candids=np.delete(self.Candids,np.where(self.Candids!=candid))
                
# def is_unique_candid(puzzle,candidate,dim,which):
#     if dim=='row' or dim=='r':
#         for i in range(0,9):
#             for k in range(0,len(puzzle[which][i].Candids-1)):
#                 if candidate==puzzle[which][i].Candids[k]:
#                     return False
#         return True
#     if dim=='col' or dim=='c':
#         for i in range(0,9):
#             for k in range(0,len(puzzle[i][which].Candids-1)):
#                 if candidate==puzzle[i][which].Candids[k]:
#                     return False
#         return True
#     if dim=='square' or dim=='s':
#         for i in range(0,3):
#             for j in range(0,3):
#                 for k in range(0,len(puzzle[3*which[0]+i][3*which[1]+j].Candids-1)):
#                     if candidate==puzzle[3*which[0]+i][3*which[1]+j].Candids[k]:
#                         return False
#         return True

def puzzle_is_solved(puzzle):
    for r in range(0,9):
        for c in range(0,9):
            if puzzle[r][c].Value==0 or len(puzzle[r][c].Candids)>0:
                return False
            
    return True


def hidden_single(puzzle, puzzle_cpy, position):
    r,c=(position)
    if not puzzle[r][c].is_trivial():
        #in row
        # if dim=='r' or dim=='row':
            for i in range(0,9):
                intersect=np.intersect1d(puzzle[r][c].Candids,puzzle[r][i].Candids)
                union=np.union1d(puzzle[r][c].Candids,puzzle[r][i].Candids)
                if len(union) == len(intersect)+1 and len(intersect)>0:
                    print(puzzle[r][c].Candids)
                    print(puzzle[r][i].Candids)
                    puzzle_cpy[r][c].remove(intersect)
                    puzzle_cpy[r][c].Value=puzzle_cpy[r][c].Candids[0]
                    puzzle_cpy[r][c].remove(puzzle_cpy[r][c].Value)
                    return
        #in column
        # if dim=='c' or dim=='col':
            for i in range(0,9):
                intersect=np.intersect1d(puzzle[r][c].Candids,puzzle[i][c].Candids)
                union=np.union1d(puzzle[r][c].Candids,puzzle[i][c].Candids)
                if len(union) == len(intersect)+1 and len(intersect)>0:
                    print(puzzle[r][c].Candids)
                    print(puzzle[i][c].Candids)
                    puzzle_cpy[r][c].remove(intersect)
                    puzzle_cpy[r][c].Value=puzzle_cpy[r][c].Candids[0]
                    puzzle_cpy[r][c].remove(puzzle_cpy[r][c].Value)
                    return
        #in region
        # if dim=='s' or dim=='square':
            square_r=r//3
            square_c=c//3
            for i in range(0,3):
                for j in range(0,3):
                    intersect=np.intersect1d(puzzle[r][c].Candids,puzzle[3*square_r+i][3*square_c+j].Candids)
                    union=np.union1d(puzzle[r][c].Candids,puzzle[3*square_r+i][3*square_c+j].Candids)
                    if len(union) == len(intersect)+1 and len(intersect)>0:
                        print(puzzle[r][c].Candids)
                        print(puzzle[3*square_r+i][3*square_c+j].Candids)
                        puzzle_cpy[r][c].remove(intersect)
                        puzzle_cpy[r][c].Value=puzzle_cpy[r][c].Candids[0]
                        puzzle_cpy[r][c].remove(puzzle_cpy[r][c].Value) 
                        return


## MAIN BODY   
        
## PREPARATION STEPS
#reading in the file
f=open('sudoku.txt','r')
#removing separators
sequence=f.read().replace('\n','').replace(' ','').replace(',','').replace(';','')
length=len(sequence)
#check number of elements
if length!=81 & length!=sequence.isdigit():
    print('Input is not in the right format or length')
vstup=np.array([s for s in sequence],dtype=np.uint8)
np.ndarray.resize(vstup,(9,9))

#create an array of classes
puzzle=np.ndarray((9,9),dtype=np.dtype(pole))
#copying stuff to the array of classes
for i in range(0,9):
    for j in range(0,9):
        puzzle[i][j]=pole(vstup[i][j])








## SOLVING STEPS
        


counter=1
while not puzzle_is_solved(puzzle) and counter<2:

    #Purging candidates
    for r in range(0,9):
        for c in range(0,9):
            if not puzzle[r][c].is_trivial():
                for i in range(0,9):
                    puzzle[i][c].remove(puzzle[r][c].Value)
                for i in range(0,9):
                    puzzle[i][c].remove(puzzle[r][c].Value)
                squares_r=r//3
                squares_c=c//3
                for i in range(0,3):
                    for j in range(0,3):
                        puzzle[3*squares_r+i][3*squares_c+j].remove(puzzle[r][c].Value)

    #Filling singles
    for r in range(0,9):
        for c in range(0,9):
            if puzzle[r][c].is_trivial():
                puzzle[r][c].Value=puzzle[r][c].Candids[0]
                puzzle[r][c].remove(puzzle[r][c].Value)
                
                
    #Filling hidden singles
    puzzle_cpy=np.copy(puzzle)
    for r in range(0,9):
        for c in range(0,9):
            print(str(r)+'x'+str(c)+'\n')
            hidden_single(puzzle,puzzle_cpy,(r,c))
    
    print(counter)
    counter+=1
    
    
    
    






#printing result        
print(puzzle_is_solved(puzzle))
print(vstup)   
print('\n')

  
vystup=np.ndarray((9,9),dtype=np.dtype('uint8'))   
vystup_cpy=np.ndarray((9,9),dtype=np.dtype('uint8'))      
for i in range(0,9):
    for j in range(0,9):
        vystup[i][j]=puzzle[i][j].Value
        vystup_cpy[i][j]=puzzle_cpy[i][j].Value
        
print(vystup)
print('\n')
print(vystup_cpy)
print('\n')