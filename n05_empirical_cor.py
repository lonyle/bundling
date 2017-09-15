# input: drv_mean_std.json, drv_copurchase_prob.csv)
# output: drv_cov.csv

import json 
import numpy as np 
from scipy.stats import mvn
from scipy.stats import norm
from multiprocessing import Process, Pool
import pandas as pd

def prob_to_correlation(prob, s, t): # s = mu_1/sigma_1, t = mu_2/sigma_2
	epsilon = 0.00001
	# search the unique correlation coefficient corresponding to the desired probability
	lower = np.array([-s, -t]) 
	upper = np.array([0, 0]) # dummy
	infin = np.array([1, 1])
	rho_left = -1
	rho_right = 1
	while rho_right - rho_left > epsilon:
		rho = (rho_left + rho_right)/2
		error, value, inform = mvn.mvndst(lower, upper, infin, np.array([rho]))
		if value < prob:
			rho_left = rho
		elif value > prob:
			rho_right = rho
		else:
			break

	return rho_left

def emprical_cor(mean_vec, price_vec, std_vec, copurchase_prob_mat):
	N_product = len(mean_vec)
	pool = Pool(processes = 8) # parallel, set as number of cores
	cor_mat = np.zeros(shape=(N_product, N_product))
	for i in range(N_product):
		if i % 100 == 0:
			print (i)
		arg_vec = []
		for j in range(N_product):
			prob = copurchase_prob_mat[i][j]
			prob = min(1, prob)

			s = (mean_vec[i]-price_vec[i])/std_vec[i]
			t = (mean_vec[j]-price_vec[j])/std_vec[j]
			arg_vec.append( (prob, s, t) )
		cor_vec = pool.starmap(prob_to_correlation, arg_vec)

		for j in range(N_product):
			cor_mat[i][j] = cor_vec[j]
			
	pool.close()
	pool.join()
	return cor_mat

if __name__ == '__main__':
	json_data = json.load(open('data/drv_mean_std.json'))
	mean_vec = json_data['mean_vec']
	std_vec = json_data['std_vec']
	products = json.load(open('data/drv_products_selected.json'))
	price_vec = []
	for product in products:
		price_vec.append(product['price'])

	copurchase_prob_mat = pd.read_csv('data/drv_copurchase_prob.csv', header=None, delimiter=',').as_matrix()

	cov_mat = emprical_cor(mean_vec, price_vec, std_vec, copurchase_prob_mat)
	np.savetxt('data/drv_cor.csv', cov_mat, delimiter=',')