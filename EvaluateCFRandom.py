import numpy as np
import pandas as pd
import sys

def get_matrix():
    return pd.read_csv('jester-data-1.csv', header=None, na_values=99).iloc[:,1:].values

def evaluate(dataMatrix,method=-1,size=1,repeats=1):
    '''
    method = Which collaborative filtering techniques will be tested
    size = number of predictions evaluated
    repeats = number of times the test is repeated
    '''
    if method == -1:
        '''
        Print list of methods
        '''
        print("List of Methods:")
        print("Id, Method-Name")
        print("1: Average Nnn ranking")
        print("2: Average Weighted Sum")
        print("3: Average Weighted Nnn Sum")
    else:
        '''
        Evaluate
        '''
        maeList = []
        for i in range(repeats):
          print("test number: {}".format(i))
          userItemTuples = getRandom(size,dataMatrix)
          sampleMAE = []
          print("userID, itemID, Actual_Rating, Predicted_Rating, Delta_Rating")
          for uTuple in userItemTuples:
              sampleMAE.append(singleMAE(uTuple,dataMatrix))
          mae = np.mean(sampleMAE)
          print("MAE for test: {} = {}\n".format(i,mae))
          maeList.append(mae)
        print('Overall Evaluation:')
        print('Mean MAE = {}'.format(np.mean(maeList)))
        print('SD MAE = {}'.format(np.std(maeList)))

def getRandom(size,dataMatrix):
    '''
    Returns a size length list of tuples
    Each tuple is a valid (UserId, ItemId)
    '''
    tupleList = []
    while(len(tupleList)<size):
        tupleList.append(getValidUserItem(dataMatrix))
    return tupleList

def getValidUserItem(dataMatrix):
    '''
    Returns a tuple (UserId, ItemId)
    That has a valid rating
    '''
    temp = np.nan
    while(np.isnan(temp)):
      ItemId = np.random.randint(0,100)
      UserId = np.random.randint(0,24983)
      temp = dataMatrix[UserId][ItemId]
    return (UserId,ItemId)

def singleMAE(userItemTuple,dataMatrix):
    pred = makePrediction(userItemTuple)
    actu = dataMatrix[userItemTuple[0]][userItemTuple[1]]
    delta = abs(actu-pred)
    print("{}, {}, {}, {}, {}".format(userItemTuple[0],userItemTuple[1],actu,pred,delta))
    return delta

def makePrediction(userItemTuple):
    return 0

if __name__ == "__main__":
  dataMatrix = get_matrix()
  if len(sys.argv) < 4:
      evaluate(dataMatrix)
  else:
      method = int(sys.argv[1])
      size = int(sys.argv[2])
      repeats = int(sys.argv[3])
      evaluate(dataMatrix,method,size,repeats)
