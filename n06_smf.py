# input: drv_cov.csv
# output: drv_cov_psd.csv

import numpy as np 
import random 
import math
import pandas as pd
import matplotlib.pyplot as plt
import sys

import time

# projected gradient descent
def smf_pgd(Cov, W, f):
	N_product = Cov.shape[0]
	# initialize
	X_mat = []
	for i in range(N_product):
		X_vec = []
		for j in range(f):
			X_vec.append(random.random())
		norm2 = math.sqrt(sum( list(map(lambda x:x**2, X_vec)) ))
		X_vec_normalized = list(map(lambda x:x/norm2, X_vec))
		X_mat.append(X_vec_normalized)

	X = np.matrix(X_mat).T 

	for i in range(N_product):
		W[i][i] = 0

	N_iteration = 100
	eta = 0.00005

	grad_sum = np.zeros( N_product )

	cost_vec = []
	for ite in range(N_iteration):
		print ('iteration', ite)
		cost = np.multiply( np.square( np.dot(X.T, X) - Cov ), W ).sum()/(N_product**2)
		cost_vec.append(cost)
		print ('Average cost:', cost)
		right_part = np.multiply( np.dot(X.T, X)-Cov, W )
		grad = np.dot(X, right_part)

		Y = X - grad * (eta/math.sqrt(ite+1))
		Y_2norm_col = np.linalg.norm(Y, axis=0)
		print ('Average 2-norm:', Y_2norm_col.sum()/N_product)
		X = Y / Y_2norm_col

	predicted_cov_mat = np.dot(X.T, X)
	plt.plot(cost_vec)
	return predicted_cov_mat, X

if __name__ == '__main__':
	f = int(sys.argv[1]) # number of features of each product
	alpha = 0.1 # baseline weight for 0 co-purcahse

	cov_mat = pd.read_csv('data/drv_cor.csv', delimiter=',', header=None).as_matrix()
	copurchase_mat = pd.read_csv('data/drv_copurchase_selected.csv', delimiter=',', header=None).as_matrix()

	N_product = cov_mat.shape[0]

	W = copurchase_mat + alpha * np.ones( (N_product, N_product) )

	predicted_cov_mat, X = smf_pgd(cov_mat, W, f)

	np.savetxt('data/drv_cov_psd.csv', predicted_cov_mat, delimiter=',')
	np.savetxt('data/drv_products_features.csv', X, delimiter=',')


