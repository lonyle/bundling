# use spectral clustering or direct method to calculate co-purchasing probability

# input: drv_copurchase_selected.csv, drv_products_selected.json
# output: drv_copurchase_prob.csv

import numpy as np 
import json
import pandas as pd

def get_copurchase_prob_mat_raw(sales_vec, copurchase_mat):
	a = 16674.27
	N_product = len(sales_vec)
	copurchase_prob_mat = np.zeros(shape=(N_product, N_product))
	sales_max = max(sales_vec)
	for i in range(N_product):
		for j in range(N_product):
			#f^{-1} function			
			copurchase_prob_mat[i][j] = np.log( (copurchase_mat[i][j]/sales_max)*(a-1)+1 ) / np.log(a)
	return copurchase_prob_mat

if __name__ == '__main__':
	products = json.load(open('data/drv_products_selected.json'))
	N_product = len(products)
	sales_vec = [None] * N_product
	for i in range(N_product):
		product = products[i]
		sales_vec[i] = product['sales_count']

	copurchase_mat = pd.read_csv('data/drv_copurchase_selected.csv', delimiter=',', header=None).as_matrix()
	
	print ('ordinary approach')
	copurchase_prob_mat_raw = get_copurchase_prob_mat_raw(sales_vec, copurchase_mat)
	np.savetxt('data/drv_copurchase_prob.csv', copurchase_prob_mat_raw, delimiter=',')
