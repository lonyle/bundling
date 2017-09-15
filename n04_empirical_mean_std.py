# input: drv_products_selected.json
# output: drv_mean_std.json

import pi

import json
import numpy as np 
from scipy.stats import norm
import matplotlib.pyplot as plt
import math
from multiprocessing import Process, Pool
from scipy.stats import norm

# fixed variance
def get_mean(delta, price, std):
	delta = min(0.99, delta)
	delta = max(0.01, delta)
	return norm.ppf(delta) * std + price

def empirical_mean_variance(products):
	N_product = len(products)
	mean_vec = [None] * N_product
	std_vec = [None] * N_product

	sales_count_vec = []
	price_vec = []
	for product in products:
		sales_count_vec.append( product['sales_count'] )
		price_vec.append(product['price'])

	print ('average price:', sum(price_vec)/len(price_vec))

	max_sales_count = max(sales_count_vec)
	print (max_sales_count)

	delta_vec = [None] * N_product
	#f^{-1} function
	a = 16674.27
	for i in range(N_product):
		delta_vec[i] = np.log( (sales_count_vec[i]/max_sales_count)*(a-1)+1 ) / np.log(a)

	print ('mean delta', sum(delta_vec)/N_product)

	std = 15 #fixed variance, you may change it to other values

	for i in range(N_product):		
		mean_vec[i] = get_mean(delta_vec[i], price_vec[i], std)
		std_vec[i] = std

	print ('mean of valuations and mean of price', sum(mean_vec)/N_product, sum(price_vec)/N_product)

	return mean_vec, std_vec, delta_vec

if __name__ == '__main__':
	products = json.load(open('data/drv_products_selected.json'))
	mean_vec, std_vec, delta_vec = empirical_mean_variance(products)

	with open('data/drv_mean_std.json', 'w') as output_file:
		json.dump({'mean_vec': mean_vec, 'std_vec': std_vec, 'delta_vec': delta_vec}, output_file, indent=4)

