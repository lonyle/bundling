# profit after bundling a set of products

import pi
import json
import os.path
import numpy as np

# use the profit without bundle as the baseline
def profit_baseline(mu_vec, Cov_mat, alpha):
	profit = 0
	N = len(mu_vec)
	for i in range(N):
		profit += pi.pi(mu_vec[i], Cov_mat[i, i], alpha, 0)[1]
	return profit

# optimal profit after bundling
def profit_bundle(bundle_set, bundle_vec, mu_vec, Cov_mat, alpha, separate_profit_vec):
	profit = 0
	N = len(mu_vec)	
	bundle_mean = 0
	bundle_variance = variance(bundle_vec, Cov_mat)
	for i in bundle_set:
		bundle_mean += mu_vec[i]

	for i in range(N):
		if i not in bundle_set:
			profit += separate_profit_vec[i]

	profit += pi.pi(bundle_mean, bundle_variance, alpha, 0)[1]
	return profit

def separate_sale_profit(mu_vec, Cov_mat, alpha):
	if os.path.isfile('data/drv_separate_profit.json'):
		separate_profit_vec = json.load(open('data/drv_separate_profit.json'))
	else:
		print ('calculating the separate sale profit...')
		N_product = len(mu_vec)
		separate_profit_vec = [None] * N_product
		
		for i in range(N_product):
			profit = pi.pi(mu_vec[i], Cov_mat[i, i], alpha, 0)[1]
			separate_profit_vec[i] = profit
		with open('data/drv_separate_profit.json', 'w') as output_file:
			json.dump(separate_profit_vec, output_file, indent=4)

	print ('baseline profit of separate sale is', sum(separate_profit_vec))

	return separate_profit_vec
		
def variance(x, C):
	return np.dot( np.dot( np.asarray(x).transpose(), C), np.asarray(x) )