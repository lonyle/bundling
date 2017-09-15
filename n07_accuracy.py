import sys
import pi

import numpy as np 
from scipy.stats import norm
from scipy.stats import mvn
import scipy.stats as stat
import json
import pandas as pd
from multiprocessing import Process, Pool
import sys

def correlation_to_prob(rho, s, t):
	lower = np.array([-s, -t]) 
	upper = np.array([0, 0]) # no use
	infin = np.array([1, 1])
	error, value, inform = mvn.mvndst(lower, upper, infin, np.array([rho]))
	return value


def evaluate_prediction(predicted_cov_mat, copurchase_mat, mean_vec, price_vec, std_vec, sales_vec, delta_vec):
	print ('evaluating the predicted covariance matrix...')
	N_product = len(mean_vec)

	# predicted probability that two products are co-purchased
	predicted_copurchase_mat = np.zeros((N_product, N_product))

	max_sales = max(sales_vec)
	
	f_delta_vec = list(map(lambda x:pi.mapping(x) * 100000, delta_vec))

	pool = Pool(processes = 8)
	for i in range(N_product):
		if i % 100 == 0:
			print (i)
		arg_vec = []
		for j in range(i, N_product):
			s = (mean_vec[i] - price_vec[i])/std_vec[i]
			t = (mean_vec[j] - price_vec[j])/std_vec[j]			
			rho = predicted_cov_mat[i][j]
			arg_vec.append( (rho, s, t) )
		value_vec = pool.starmap(correlation_to_prob, arg_vec)

		for j in range(i, N_product):
			value = value_vec[j - i] # minus the index
			
			predicted_copurchase_mat[i][j] = value # we do not do the mapping because the rank doesn't change
			predicted_copurchase_mat[j][i] = predicted_copurchase_mat[i][j]

	pool.close()
	pool.join()

	rank_vec = [None] * N_product
	for i in range(N_product):
		predicted_copurchase_vec = predicted_copurchase_mat[i]
		rank_vec[i] = list(stat.rankdata(predicted_copurchase_vec) )

	rank_mat = np.matrix(rank_vec)

	total_rank = np.multiply(rank_mat, copurchase_mat).sum()
	copurchase_sum = copurchase_mat.sum()

	average_rank = total_rank/copurchase_sum/N_product
	return 1 - average_rank #because we sort reversely

if __name__ == '__main__':
	print ('loading the cov matrix...')
	predicted_cov_mat = pd.read_csv('data/drv_cov_psd.csv', delimiter=',', header=None).as_matrix()
	print ('loading the co-purchase matrix...')
	copurchase_mat = pd.read_csv('data/drv_copurchase_selected.csv', delimiter=',', header=None).as_matrix()
	print ('loading products data')
	json_data = json.load(open('data/drv_mean_std.json'))
	mean_vec = json_data['mean_vec']
	std_vec = json_data['std_vec']
	delta_vec = json_data['delta_vec']

	products = json.load(open('data/drv_products_selected.json'))

	price_vec = []
	sales_vec = []
	for product in products:
		price_vec.append(product['price'])
		sales_vec.append(product['sales_count'])

	accuracy = evaluate_prediction(predicted_cov_mat, copurchase_mat, mean_vec, price_vec, std_vec, sales_vec, delta_vec)
	print ('accuracy:', accuracy)
	with open('data/result_accuracy_' + str(sys.argv[1]) + '.json', 'w') as output_file:
		json.dump(accuracy, output_file)
	