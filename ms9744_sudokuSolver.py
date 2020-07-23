#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 15:03:06 2019

@author: mikesingh1098
"""

#!/usr/bin/python3 

def fileRead(inputFile):
    "Reads the file, and allocates the integers into one list"
    puzzleFull = []
    "for each line"
    for i in inputFile:
        if i != '\n':
            "add only integers, and ignore the junk"
            puzzle = []
            puzzle.append(int(i[0]))
            puzzle.append(int(i[2]))
            puzzle.append(int(i[4]))
            puzzle.append(int(i[6]))
            puzzle.append(int(i[8]))
            puzzle.append(int(i[10]))
            puzzle.append(int(i[12]))
            puzzle.append(int(i[14]))
            puzzle.append(int(i[16]))
            puzzleFull.append(puzzle)
    return puzzleFull

#writes solution in to output file, but if grid is incomplete, there is no solution
def fileOutput(outFile,grid):
  try:
      for row in grid:
          line = ""
          for num in row:
              line += str(num)+" "
          outFile.write(line)
          outFile.write('\n')
  except:
      outFile.write("No Solution found")

#copies grid
def gridCopy(grid):
  return [row[:] for row in grid]

#checks for validity within its row 
def rowValidity(grid):
  for row in grid:
    numbersSeen = []
    for num in row:
      if num == 0:
        continue
      if num in numbersSeen:
        return False
      numbersSeen.append(num)
  return True

#checks if any two unassigned are in same subgrid
def checkInSameSubGrid(grid,unassigned1,unassigned2):

  indI1 = unassigned1[0]//3
  indJ1= unassigned1[1]//3
  indI2 = unassigned2[0]//3
  indJ2 = unassigned2[1]//3
  
  if indI1 == indI2 and indJ1 ==indJ2:
      return True
  else:
      return False
  
#checks for validity within its column, by using the rowsValidity function
def columnValidity(grid):
  columns = []
  for i in range(9):
      singleColumn = []
      for j in range(9):
          singleColumn.append(grid[j][i])
      columns.append(singleColumn)
  return rowValidity(columns)


#checks if any numbers in possible domain conflicts with its subgrid
def subGridValidity(grid):
  
  m = 3
  
  for i in range(m):
    for j in range(m):
      subGrid = [row[j*m:(j+1)*m] for row in grid[i*m:(i+1)*m]]
      #sub_grid = []
      #for row in grid[i*m:(i+1)*m]:
       #   sub_grid.append(row[j*m:(j+1)*m])
      total = set()
      for row in subGrid:
        for num in row:
          if num == 0:
            continue
          if num in total:
            return False
          total.add(num)
  return True

#implementation of MRV heuristic
def constrainedSquare(grid,unassigned):
    gridHolder = gridCopy(grid)
    domainHolder = []
    count = 0
    for i in range(1,10):
        indI = int(unassigned[0])
        indJ = int(unassigned[1])
        gridHolder[indI][indJ] = i
        gridValidCheck = rowValidity(gridHolder) and columnValidity(gridHolder) and subGridValidity(gridHolder)
        if (gridValidCheck):
            count+=1
            domainHolder.append(i)
    unassigned[4] = domainHolder
    unassigned[2] = count
    return unassigned[2]

#implementation of degree heuristic
def degreeHeurSquares(grid,unassList):
    for i in range(len(unassList)):
        count = 0
        for j in range(len(unassList)):
            if (unassList[j][1] == unassList[i][1] or unassList[j][0] == unassList[i][0] or checkInSameSubGrid(grid,unassList[j],unassList[i])):
                count+=1
        unassList[i][3] = count-1
    return

#checks if we have come to the solution
def solutionCheck(grid):
  return sum([row.count(0) for row in grid]) == 0

#picks next spot based off heuristics
def pickNextSpot(grid,unassList):
    degreeHeurSquares(grid,unassList)
    minVal = 10
    unassHold = []
    for i in range(len(unassList)):
        constrainedSquare(grid,unassList[i])
        if (unassList[i][2]<minVal):
            minVal = unassList[i][2]
            unassHold= unassList[i]
        if (unassList[i][2] == minVal):
            if (unassList[i][3] > unassHold[3]):
                minVal = unassList[i][2]
                unassHold = unassList[i]
    return unassHold

#The end grid or solution
finalGrid = None 

#solver glue for the sudoku problem
def solver(grid, spotCurrent, unassigned, x):
  global finalGrid

  #all unassigned are assigned
  if len(unassigned) == 0:
    return

  # the solution has already been found through another process
  if finalGrid != None:
    return

  #if the domain of an unassigned is 0, quit the program as there is no solution
  for i in unassigned:
      if (len(i[4]) == 0):
          return
      
  # grid did not pass validity checks (should never happen but good to hold on to in case)
  is_grid_valid = rowValidity(grid) and columnValidity(grid) and subGridValidity(grid)
  if is_grid_valid == False:
    return

  #set the grid indices of the unassigned to the requested value
  unassHold = spotCurrent
  unassPlace = unassigned
  grid[unassHold[0]][unassHold [1]] = x
  unassPlace.remove(unassHold )
  

  # we hit the solution, so return
  is_grid_solved = solutionCheck(grid)
  if is_grid_solved == True:
    finalGrid = grid
    return

  #not solved yet, but passes validity checks so keep going
  unassNow = pickNextSpot(grid,unassigned)
  #recurse on the domain from least to greatest
  for x in unassNow[4]:
      spotCurr = unassNow
      solver(gridCopy(grid), spotCurr, unassPlace, x)

def main():
    "Read in file, and create a list"
    file = open("Tests/SUDOKU_input1.txt","r")
    fileToRead = file.readlines()
    grid = fileRead(fileToRead)
    "Create Output File"
    outFile = open("Tests/SUDOKU_Output1.txt","w")
    
    #unassigned variables initialization
    unassigned = []
    constraints = 0
    degree = 0
    domain = []
    for i in range(9):
        for j in range(9):
          if grid[i][j] == 0:
            unassigned.append([i, j, constraints, degree, domain])
        
    spotNow = pickNextSpot(grid,unassigned)
    #first iteration into solver  
    for x in spotNow[4]:
        spotPlace = unassigned
        spotCurrent = spotNow
        solver(gridCopy(grid), spotCurrent, spotPlace, x)
    
    #output answer
    fileOutput(outFile,finalGrid)
    
main()


  
  