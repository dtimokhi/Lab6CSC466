import numpy as np
import pandas as pd
import copy
import sys


class JokerObject:
    def __init__(self, matrix):
        self.matrix = matrix
        self.item_means = np.nanmean(matrix, 0)
        self.user_means = np.nanmean(matrix, 1)

    def get_matrix(self):
        return self.matrix

    def get_items_m(self):
        return self.item_means

    def get_item_m(self, key):
        return self.item_means[key]

    def get_users_m(self):
        return self.user_means

    def get_user_m(self, key):
        return self.user_means[key]

    def get_item(self, row, col):
        return self.matrix[row][col]

    def set_object_nan(self, row, col):
        self.matrix[row][col] = np.nan

    def get_pearson_matrix(self):
        distances = np.zeros((len(self.item_means), len(self.item_means)))
        transposes = self.matrix.transpose()
        t0 = dt.datetime.now()
        for i, item_1 in enumerate(transposes):
            if i % 1 == 0:
                print(i)
                print("time: ", dt.datetime.now() - t0)
            for j, item_2 in enumerate(transposes):
                if (i > j):
                    continue
                if i != j:
                    top = np.sum((a - self.item_means[i]) * (b - self.item_means[j]) for a, b in zip(item_1, item_2) if
                                 np.isnan(a) == False and np.isnan(b) == False)
                    bot = np.sqrt(np.sum(np.square(a - self.item_means[i]) for index, a in enumerate(item_1) if
                                         np.isnan(a) == False and np.isnan(item_2[index]) == False) * np.sum(
                        np.square(b - self.item_means[j]) for index, b in enumerate(item_2) if
                        np.isnan(b) == False and np.isnan(item_1[index]) == False))
                    distances[i, j] = top / bot
                    distances[j, i] = distances[i, j]
        return distances

'''
    Distance matrix 100 x 100 by items
    coords is (user, item) to guess
'''
def get_avg_weighted_sum(distance_matrix, data_matrix, coords):
    if not np.isnan(data_matrix.get_item(coords[0],coords[1])):
        data_matrix = copy.deepcopy(data_matrix)
        data_matrix.set_object_nan(coords[0],coords[1])
    return data_matrix.get_item_m(coords[1]) + (1/distance_matrix.sum(axis=0)[coords[1]])*np.sum(distance_matrix[coords[1]][c_prime]*(data_matrix.get_item(coords[0], c_prime)-data_matrix.get_item_m(c_prime))for c_prime in range(distance_matrix.shape[0]) if not np.isnan(data_matrix.get_item(coords[0], c_prime)))


def get_average_ranking(data_matrix, coords):
    if not np.isnan(data_matrix.get_item(coords[0],coords[1])):
        data_matrix = copy.deepcopy(data_matrix)
        data_matrix.set_object_nan(coords[0],coords[1])
    utilities = [data_matrix.get_item(c,coords[1])for c in range(data_matrix.get_matrix().shape[0]) if not np.isnan(data_matrix.get_item(c, coords[1]))]
    return (1/len(utilities))*sum(utilities)

def get_adjusted_weighted_Nnn_sum(distance_matrix, data_matrix, coords, N = 3):
    if not np.isnan(data_matrix.get_item(coords[0],coords[1])):
        data_matrix = copy.deepcopy(data_matrix)
        data_matrix.set_object_nan(coords[0],coords[1])
    return data_matrix.get_item_m(coords[1]) + (1/distance_matrix.sum(axis=0)[coords[1]])*np.sum(distance_matrix[coords[1]][c_prime]*(data_matrix.get_item(coords[0], c_prime)-data_matrix.get_item_m(c_prime))for c_prime in dist[coords[1],].argsort()[:N] if not np.isnan(data_matrix.get_item(coords[0], c_prime)))

def makePrediction(userItemTuple,method,dataMatrix):
    methods = {1:get_average_ranking,2:get_avg_weighted_sum,3:get_adjusted_weighted_Nnn_sum}
    jokerDataMatrix = JokerObject(dataMatrix)
    return methods[method](jokerDataMatrix,userItemTuple)

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
              sampleMAE.append(singleMAE(uTuple,dataMatrix,method))
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
    shapeDM = dataMatrix.shape
    while(np.isnan(temp)):
      ItemId = np.random.randint(0,shapeDM[1])
      UserId = np.random.randint(0,shapeDM[0])
      temp = dataMatrix[UserId][ItemId]
    return (UserId,ItemId)

def singleMAE(userItemTuple,dataMatrix,method):
    pred = makePrediction(userItemTuple,method,dataMatrix)
    actu = dataMatrix[userItemTuple[0]][userItemTuple[1]]
    delta = abs(actu-pred)
    print("{}, {}, {}, {}, {}".format(userItemTuple[0],userItemTuple[1],actu,pred,delta))
    return delta

if __name__ == "__main__":
  dataMatrix = get_matrix()
  if len(sys.argv) < 4:
      evaluate(dataMatrix)
  else:
      method = int(sys.argv[1])
      size = int(sys.argv[2])
      repeats = int(sys.argv[3])
      evaluate(dataMatrix,method,size,repeats)
