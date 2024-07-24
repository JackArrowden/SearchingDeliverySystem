import random

def checkOpenFile(file):
    try:
        with open(file, 'r') as cur:
            return True
    except:
        return False

def autoFindGoal(mat, listSs, listGs): # Does not account for Fuel stations because they are represented as -2
    result = []
    n = len(mat)
    m = len(mat[0])
    for i in range(n):
        for j in range(m):
            if mat[i][j] >= 0 and [i, j] not in listSs and [i, j] not in listGs:
                result.append([i, j])
    return random.sample(result, len(listSs) - len(listGs))

def readInput(file):
    try:
        curFile = open(file, 'r')
        strArray = curFile.readline().strip().split()
            
        n = int(strArray[0])
        m = int(strArray[1])
        t = int(strArray[2]) if len(strArray) >= 3 else None
        f = int(strArray[3]) if len(strArray) == 4 else None
            
        cityMap = []
        points = []
        index = []
        startPoints = []
        goalPoints = []
        fuel = []
        
        for i in range(n):
            strArray = curFile.readline().strip().split()
            curRow = []
            
            for j in range(m):
                letter = strArray[j]
                if letter.isdigit() or letter[0] == '-':
                    curRow.append(int(letter))
                    continue
                
                if len(letter) == 1:
                    letter = letter + '0'
                letter2 = int(letter[1])
                    
                if letter[0] == 'S':
                    curRow.append(0)   
                    if int(letter2) not in index:
                        index.append(int(letter2))
                        points.append([int(letter2)])
                    points[index.index(int(letter2))].insert(1, [i, j]) # A list or a tuple? Starting from 0 or 1?
                elif letter[0] == 'G':
                    curRow.append(0)   
                    if letter2 not in index:
                        index.append(int(letter2))
                        points.append([int(letter2)])
                    points[index.index(int(letter2))].append([i, j])
                elif letter[0] == 'F':
                    curRow.append(-1 - int(letter2))
                    fuel.append([i, j])   
                    
            cityMap.append(curRow)
            
        points.sort()
        startPoints = [point[1] for point in points]
        goalPoints = [point[2] for point in points if len(point) == 3]
        
        if len(startPoints) != len(goalPoints): # In case some goals are not represented in the input file
            listPoints = autoFindGoal(cityMap, startPoints, goalPoints)
            goalPoints.clear()
            goalPoints = [point[2] if len(point) == 3 else listPoints.pop() for point in points]
        
        return (cityMap, startPoints, goalPoints) if t == None else (cityMap, startPoints, goalPoints, t) if f == None else (cityMap, startPoints, goalPoints, t, f, fuel)
            
    finally:
        curFile.close()
          
def writeOutput(file, listPath):
    curFile = open(file, 'w')

    for cur in listPath:
        curFile.write(cur[0] + '\n')
        for point in cur[1]:
            curFile.write(str(point))
            curFile.write(' ')
        curFile.write('\n')
            
    curFile.close()
    return

# print(readInput('input.txt'))