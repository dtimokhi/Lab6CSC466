import numpy as np
import pandas as pd
import EvaluateCFRandom as helper
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
        distances = np.zeros((len(self.user_means),len(self.user_means)))
        for i, user_1 in enumerate(self.matrix):
            for j, user_2 in enumerate(self.matrix):
                if(i>j):
                    continue
                if i != j:
                    distances[i,j] = np.sum((a-self.user_means[i])*(b-self.user_means[j]) for a,b in zip(user_1,user_2) if np.isnan(a)== False and np.isnan(b) == False)/np.sqrt(np.sum(np.square(a-self.user_means[i]) for index, a in enumerate(user_1) if np.isnan(a)== False and np.isnan(user_2[index]) == False)*np.sum(np.square(b-self.user_means[j]) for index, b in enumerate(user_2) if np.isnan(b)== False and np.isnan(user_1[index]) == False))
                    distances[j,i] = distances[i,j]
        return distances
                    
def get_avg_weighted_sum(distance_matrix, data_matrix, coords):
    if not np.isnan(data_matrix.get_item(coords[0],coords[1])):
        data_matrix = copy.deepcopy(data_matrix)
        data_matrix.set_object_nan(coords[0],coords[1])
    return data_matrix.get_user_m(coords[0]) + (1/distance_matrix.sum(axis=0)[coords[0]])*np.sum(distance_matrix[coords[0]][c_prime]*(data_matrix.get_item(c_prime, coords[1])-data_matrix.get_user_m(c_prime))for c_prime in range(distance_matrix.shape[0]) if not np.isnan(data_matrix.get_item(c_prime, coords[1])))

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
    return data_matrix.get_user_m(coords[0]) + (1/distance_matrix.sum(axis=0)[coords[0]])*np.sum(distance_matrix[coords[0]][c_prime]*(data_matrix.get_item(c_prime, coords[1])-data_matrix.get_user_m(c_prime))for c_prime in dist[coords[0],].argsort()[:N] if not np.isnan(data_matrix.get_item(c_prime, coords[1])))

def get_matrix():
    return pd.read_csv('jester-data-1.csv', header=None, na_values=99).iloc[:,1:].values

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
  dataMatrix = get_matrix()
  if len(sys.argv) < 3:
      evaluate(dataMatrix)
  else:
      method = int(sys.argv[1])
      list = sys.argv[2]
      evaluate(dataMatrix,method,list)
