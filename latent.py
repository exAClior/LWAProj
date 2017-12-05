import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from random import randint
from random import shuffle
import math
import redis

class MF():

    def __init__(self, R, K, alpha, beta, iterations):
        """
        Perform matrix factorization to predict empty
        entries in a matrix.

        Arguments
        - R (ndarray)   : user-item rating matrix
        - K (int)       : number of latent dimensions
        - alpha (float) : learning rate
        - beta (float)  : regularization parameter
        """

        self.R = R
        self.num_users, self.num_items = R.shape
        self.K = K
        self.alpha = alpha
        self.beta = beta
        self.iterations = iterations

    def train(self):
        # Initialize user and item latent feature matrice
        self.P = np.random.normal(scale=1./self.K, size=(self.num_users, self.K))
        self.Q = np.random.normal(scale=1./self.K, size=(self.num_items, self.K))

        # Initialize the biases
        self.b_u = np.zeros(self.num_users)
        self.b_i = np.zeros(self.num_items)
        self.b = np.mean(self.R[np.where(self.R != 0)])

        # Create a list of training samples
        self.samples = [
            (i, j, self.R[i, j])
            for i in range(self.num_users)
            for j in range(self.num_items)
            if self.R[i, j] > 0
        ]

        # Perform stochastic gradient descent for number of iterations
        training_process = []
        for i in range(self.iterations):
            shuffle(self.samples)
            self.sgd()
            mse = self.mse()
            training_process.append((i, mse))
            if (i+1) % 10 == 0:
                print("Iteration: %d ; error = %.4f" % (i+1, mse))

        return training_process

    def mse(self):
        """
        A function to compute the total mean square error
        """
        xs, ys = self.R.nonzero()
        predicted = self.full_matrix()
        error = 0
        for x, y in zip(xs, ys):
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
        Computer the full matrix using the resultant biases, P and Q
        """
        return mf.b + mf.b_u[:,np.newaxis] + mf.b_i[np.newaxis:,] + mf.P.dot(mf.Q.T)

def gen():
    nums = [x for x in range(20)]
    R = np.zeros((50,20))
    for i in range (0,50):
        shuffle(nums)
        for j in range(0,3):
            R[i][nums[j]] = randint(1,5)
    return R

if __name__ == "__main__":
    R = gen()
    names = [  'Jaylan', 'Gonzalez', 'Leonel', 'Duarte', 'Marques', 'Conrad', 'Isabella', 'Brady', 'Adelaide', 'Lynch', 'Paul', 'Adams', 'Harper', 'Gould', 'Gracie', 'Strong', 'Campbell', 'Maldonado', 'Maxwell', 'Ramsey', 'Tristan', 'Watkins', 'Matthew', 'Lester', 'Efrain', 'Arellano', 'Marely', 'Bass', 'Adolfo', 'Miranda', 'Janae', 'Farley', 'Sherlyn', 'Hartman', 'Makena', 'Barker', 'Adalynn', 'Church', 'Hunter', 'Keller', 'Kendra', 'Browning', 'Peter', 'Mendez', 'Jasiah', 'Russo', 'Makaila', 'Coffey', 'Bryan', 'Francis', 'Aracely', 'Melton', 'Meredith', 'Edwards', 'Jamal', 'Fowler', 'Rodolfo', 'Cherry', 'Bryson', 'York', 'Kaylah', 'Ibarra', 'Reginald', 'Padilla', 'Kyleigh', 'Hinton', 'Gianna', 'Khan', 'Kaeden', 'Murray', 'Clinton', 'Herman', 'Immanuel', 'Parsons', 'Ada', 'Cowan', 'Elisha', 'Mata', 'Mallory', 'Hawkins', 'Randy', 'Mahoney', 'Micaela', 'Berger', 'Ireland', 'Fernandez', 'Presley', 'Anthony', 'Alexander', 'Tyler', 'Kayley', 'Ross', 'Zachariah', 'Perry', 'Toby', 'Hamilton', 'Charlie', 'Grimes', 'Branson', 'Hoover' ]
    mf = MF(R, K=10, alpha=0.1, beta=0.01, iterations=500)
    np.savetxt('origin.txt',R,fmt='%3f')
    training_process = mf.train()
    np.savetxt('after.txt',mf.full_matrix(),fmt='%3f')
    intermediate = mf.full_matrix()-R
    ans = np.zeros((50,50))
    ans = ans + 1000
    for i in range (0,50):
        for j in range (i+1,50):
            temp = intermediate[i] - intermediate[j]
            tAns = temp.dot(temp.T)
            ans[i][j] = ans[j][i] = tAns

    diYi = np.argmin(ans,axis = 1)
    for i in range (0,50):
        ans[i][diYi[i]] = 1000

    diEr = np.argmin(ans,axis = 1)
    for i in range (0,50):
        ans[i][diEr[i]] = 1000
    diSan = np.argmin(ans,axis = 1)        

    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    
    for i in range(0,50):
        r.lpush(names[i],[names[diYi[i]],names[diEr[i]],names[diSan[i]]])
        
    print r.lrange(names[5],0,2)
    print r.lrange(names[5],0,2)
    print r.lrange(names[6],0,2)

    
    
    
