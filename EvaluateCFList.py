import numpy as np
import pandas as pd
import EvaluateCFRandom as helper
import sys

def evaluate(dataMatrix,method=-1,list=""):
    '''
    method = Which collaborative filtering techniques will be tested
    list = path to file which contains a list of tuples(UserID,ItemID)
    '''
    if method == -1 or list=="":
        '''
        Print list of methods
        '''
        print("List of Methods:")
        print("Id, Method-Name")
        print("1: Average Weighted Sum")
        print("2: Average Weighted Nnn Sum")
        print("3: Cosine Similarity/Average Weighted Nnn Sum")
    else:
        '''
        Evaluate
        '''
        userItemTuples = readList(dataMatrix,list)
        if userItemTuples == -1:
            return
        print("Evaluation on list:")
        sampleMAE = []
        print("userID, itemID, Actual_Rating, Predicted_Rating, Delta_Rating")
        for uTuple in userItemTuples:
         sampleMAE.append(helper.singleMAE(uTuple,dataMatrix))
        mae = np.mean(sampleMAE)
        print("MAE = {}\n".format(mae))

def readList(dataMatrix,list):
  f = open(list,'r')
  userItemTupleList = []
  for line in f:
    idList = line.strip().split(', ')
    userId = int(idList[0])
    itemId = int(idList[1])
    if(np.isnan(dataMatrix[userId][itemId])):
        print("Only use valid (userId, itemId) tuples!")
        print("User: {} hasn't rated Item: {}".format(userId,itemId))
        return -1
    else:
        userItemTupleList.append((userId,itemId))
  f.close()
  return userItemTupleList

if __name__ == "__main__":
  dataMatrix = helper.get_matrix()
  if len(sys.argv) < 3:
      evaluate(dataMatrix)
  else:
      method = int(sys.argv[1])
      list = sys.argv[2]
      evaluate(dataMatrix,method,list)
