import numpy as np
from random import randint
from random import shuffle
import math
import redis
import time
from concurrent import futures

import grpc
import matcher_pb2
import matcher_pb2_grpc
import requester_pb2
import requester_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

"""
Did not want to rebuild the wheel
modified the latent factor model algorithm from
http://www.albertauyeung.com/post/python-matrix-factorization/
"""

# make the matrix that has every one's preference ranking a global matrix
R = []
id_dict = {} # key = id, value = matrix row number
id_dict_reverse = {} # key = matrix row number , value = id
rdb = redis.StrictRedis(host='localhost', port=6379, db=0)

class MF():

    def __init__(self, R):

        self.R = R #user entered ranking matrix
        self.num_users, self.num_items = R.shape
        self.K = self.num_items - 5 #latent factor dimension
        self.alpha = 0.1 #learning rate
        self.beta = 0.01 # regularization parameter

    def train(self):
        # Initialize user and item latent feature matrice
        self.P = np.random.normal(scale = 1. / self.K, size = (self.num_users, self.K))
        self.Q = np.random.normal(scale = 1. / self.K, size = (self.num_items, self.K))

        # Initialize the biases
        self.b_u = np.zeros(self.num_users)
        self.b_i = np.zeros(self.num_items)
        self.b = np.mean(self.R[np.where(self.R != 0)])

        # Create a list of training samples
        self.samples = []
        for i in range(0, self.num_users):
            for j in range(0, self.num_items):
                if(self.R[i,j]) > 0:
                    self.samples.append((i,j,self.R[i,j]))


        #let the training run for at most 3 minutes
        timeout = 180
        timeoutStart = time.time()

        while time.time() < timeoutStart + timeout:
            shuffle(self.samples)
            self.sgd()
            mse = self.mse()
            #if
            if mse <= 0.01:
                break

        return None

    def mse(self):
        """
        Compute mean sqaure error between
        original matrix R and predicted matrix
        for all values in R that is non-zero
        """
        xs, ys = self.R.nonzero()
        predicted = self.full_matrix()
        error = 0
        for x in xs:
            for y in ys:
                error += pow(self.R[x, y] - predicted[x, y], 2)
        return np.sqrt(error)

    def sgd(self):
        """
        Perform stochastic graident descent
        """
        for i, j, r in self.samples:
            # Computer prediction and error
            prediction = self.get_rating(i, j)
            e = (r - prediction)

            # Update biases
            self.b_u[i] += self.alpha * (e - self.beta * self.b_u[i])
            self.b_i[j] += self.alpha * (e - self.beta * self.b_i[j])

            # Update user and item latent feature matrices
            self.P[i, :] += self.alpha * (e * self.Q[j, :] - self.beta * self.P[i,:])
            self.Q[j, :] += self.alpha * (e * self.P[i, :] - self.beta * self.Q[j,:])

    def get_rating(self, i, j):
        """
        Get the predicted rating of user i and item j
        """
        prediction = self.b + self.b_u[i] + self.b_i[j] + self.P[i, :].dot(self.Q[j, :].T)
        return prediction

    def full_matrix(self):
        """
        Computer the full matrix using the resultant bias matrix, P and Q
        """
        return mf.b + mf.b_u[:,np.newaxis] + mf.b_i[np.newaxis:,] + mf.P.dot(mf.Q.T)


#simulate the data
def gen(int num_users):
    nums = [x for x in range(20)]
    R = np.zeros((num_users,20))
    for i in range (0,num_users):
        shuffle(nums)
        for j in range(0,3):
            R[i][nums[j]] = randint(1,5)
    return R



class Recommender(recommender_pb2_grpc.RecommenderServicer):

  def Recommender(self, request, context):
    reply = recommender_pb2.UserList()
	reply.userID = request.userID
    if request.userID in id_dict:
        reply.recommendedID = rdb.lrange(request.userID,0,1)
    else:
        reply.recommendedID = {'N/A','N/A','N/A'}
	return reply

def getRanking(int serverId):
    channel = grpc.insecure_channel('23.236.49.28:50051')#IP address for AWS server
    stub = requester_pb2_grpc.RequesterStub(channel)
    try:
        response = stub.Reuqest(requester_pb2.WhichUser(serverID = serverId))
        
        return None
    except grpc.RpcError:
        return None

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  recommender_pb2_grpc.add_RecommenderServicer_to_server(Recommender(), server)
  server.add_insecure_port('[::]:50021')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == "__main__":

    mf = MF(R)
    #np.savetxt('origin.txt',R,fmt='%3f')
    mf.train()
    #np.savetxt('after.txt',mf.full_matrix(),fmt='%3f')
    intermediate = mf.full_matrix()-R
    userNum , labelNum = intermediate.shape
    ans = np.zeros((userNum,userNum)) #number of users
    ans = ans + 1000
    for i in range (0,userNum):
        for j in range (i+1,userNum):
            temp = intermediate[i] - intermediate[j]
            tAns = temp.dot(temp.T)
            ans[i][j] = ans[j][i] = tAns

    diYi = np.argmin(ans,axis = 1)
    for i in range (0,userNum):
        ans[i][diYi[i]] = 1000

    diEr = np.argmin(ans,axis = 1)
    for i in range (0,userNum):
        ans[i][diEr[i]] = 1000
    diSan = np.argmin(ans,axis = 1)

    for i in range(0,userNum):
        rdb.delete(id_dict_reverse[i])
        rdb.lpush(id_dict_reverse[i],[id_dict_reverse[diYi[i]],id_dict_reverse[diEr[i]],id_dict_reverse[diSan[i]]])
