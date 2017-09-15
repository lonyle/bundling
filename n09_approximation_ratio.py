# randomly select N products in the amazon dataset, the global optimal is found bruteforcely

import kbundle
import profit
import json
import pandas as pd
import numpy as np
import math
import time

import itertools

from multiprocessing import Process, Pool

def opt_enumerate(mean_vec, cov_mat, k, separate_profit_vec):
	alpha = 0 #dummy
	N = len(mean_vec)
	products = list(range(N))
	max_profit = -math.inf
	opt_bundle = None
	for bundle_set in itertools.combinations(products, k):
		bundle_vec = [0] * N
		for i in bundle_set:
			bundle_vec[i] = 1
		revenue = profit.profit_bundle(bundle_set, bundle_vec, mean_vec, cov_mat, alpha, separate_profit_vec)
		if revenue > max_profit:
			max_profit = revenue
			opt_bundle = bundle_set

	return float(max_profit)

if __name__ == '__main__':
	print ('loading the files...')
	json_data = json.load(open('data/drv_mean_std.json'))
	mean_vec = json_data['mean_vec']
	std_vec = json_data['std_vec']
	correlation_mat = pd.read_csv('data/drv_cov_psd.csv', delimiter=',', header=None).as_matrix()
	N_product = len(mean_vec)

	std_array = np.asarray(std_vec).reshape((len(std_vec), 1))
	std_scale_mat = np.dot(std_array, np.transpose(std_array))
	cov_mat = np.multiply(correlation_mat, std_scale_mat).astype(np.double)

	alpha = 0 # dummy

	# precompute the separate sale profit
	separate_profit_vec = profit.separate_sale_profit(mean_vec, cov_mat, alpha)

	N_vec = [20]
	k_vec = [2, 3, 4, 5, 6, 7, 8, 9]
	sample_size = 24
	result_vec = []
	pool = Pool(processes = 8)
	for N in N_vec:
		print ("N =", N)
		for k in k_vec:
			print (">> k =", k)
			profit_algo_vec = []

			arg_vec = []
			running_time_algo_vec = []
			for s in range(sample_size):
				rand_indices = list(np.random.choice(N_product, N))
				mean_vec_sub = [mean_vec[i] for i in rand_indices]
				cov_mat_sub = cov_mat[:, rand_indices][rand_indices]
				separate_profit_vec_sub = [separate_profit_vec[i] for i in rand_indices]

				start_time = time.time()
				_, profit_algo = kbundle.Kbundle_QP_relaxation(mean_vec_sub, cov_mat_sub, alpha, k, separate_profit_vec_sub)
				running_time_algo = time.time() - start_time
				running_time_algo_vec.append(running_time_algo)

				arg_vec.append((mean_vec_sub, cov_mat_sub, k, separate_profit_vec_sub))
				
				profit_algo_vec.append( float(profit_algo) )

			print ('N = ', N, 'k = ', k)

			start_time = time.time()
			profit_opt_vec = pool.starmap(opt_enumerate, arg_vec)
			profit_opt_vec = list(profit_opt_vec)
			running_time_enumerate = time.time() - start_time

			ratio_vec = list(map(lambda x,y:x/y, profit_algo_vec, profit_opt_vec))

			result = {
				'N': N,
				'k': k,
				'profit_algo_vec': list(profit_algo_vec),
				'profit_opt_vec': list(profit_opt_vec),
				'ratio_vec': ratio_vec,
				'running_time_algo': sum(running_time_algo_vec) / sample_size,
				'running_time_enumerate': running_time_enumerate / sample_size
			}
			print ('average ratio:', sum(ratio_vec)/sample_size)
			with open('data/result_heterogeneous_' + str(N) + '_' + str(k) +'.json', 'w') as output_file:
				json.dump(result, output_file, indent=4)
			result_vec.append(result)

	with open('data/result_approximation.json', 'w') as output_file:
		json.dump(result_vec, output_file, indent=4)


