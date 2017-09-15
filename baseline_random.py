import exp_setting

import profit
import json
import pandas as pd
import numpy as np 

if __name__ == '__main__':
	print ('loading the files...')
	json_data = json.load(open('data/drv_mean_std.json'))
	mean_vec = json_data['mean_vec']
	std_vec = json_data['std_vec']
	correlation_mat = pd.read_csv('data/drv_cov_psd.csv', delimiter=',', header=None).as_matrix()

	std_array = np.asarray(std_vec).reshape((len(std_vec), 1))
	std_scale_mat = np.dot(std_array, np.transpose(std_array))
	cov_mat = np.multiply(correlation_mat, std_scale_mat).astype(np.double)

	alpha = 0 # dummy

	# precompute the separate sale profit
	separate_profit_vec = profit.separate_sale_profit(mean_vec, cov_mat, alpha)

	N = len(mean_vec)

	bundle_size_vec = exp_setting.bundle_size_vec
	profit_vec = []
	sample_size = 50
	for k in bundle_size_vec:
		print ('bundle size:', k)

		sample_revenue_vec = []
		for s in range(sample_size):
			choices = np.random.choice(N, k)
			bundle_set = set(choices)
			bundle_vec = [0] * N
			for i in range(N):
				if i in bundle_set:
					bundle_vec[i] = 1

			revenue = profit.profit_bundle(bundle_set, bundle_vec, mean_vec, cov_mat, alpha, separate_profit_vec)
			print ('profit:', revenue)
			sample_revenue_vec.append(revenue)

		profit_vec.append( sum(sample_revenue_vec)/len(sample_revenue_vec) )

	with open('data/result_baseline_random_profits.json', 'w') as output_file:
		json.dump({"bundle_size_vec": bundle_size_vec, "profit_vec": profit_vec}, output_file, indent=4)		

