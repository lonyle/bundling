# determine the parameter a in f(.) function

import json
import numpy as np
import matplotlib.pyplot as plt

def average_delta(a, sales_count_vec):
	max_sales_count = max(sales_count_vec)
	N_product = len(sales_count_vec)
	delta_vec = [None] * N_product
	for i in range(N_product):
		delta_vec[i] = np.log( (sales_count_vec[i]/max_sales_count)*(a-1)+1 ) / np.log(a)

	return (sum(delta_vec)/N_product)

def search(sales_count_vec):
	epsilon = 0.0001
	a_left = 0
	a_right = 20000
	while a_right - a_left > epsilon:
		a = (a_left+a_right)/2
		print (a)
		average = average_delta(a, sales_count_vec)
		if average > 0.5: # should decrease a
			a_right = a
		elif average < 0.5:
			a_left = a
		else:
			break
	return a

if __name__ == '__main__':
	products = json.load(open('data/drv_products_selected.json'))

	sales_count_vec = []
	for product in products:
		sales_count_vec.append( product['sales_count'] )

	a = search(sales_count_vec)
	print ('the parameter $a$ is:', a)




