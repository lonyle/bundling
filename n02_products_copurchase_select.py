# input: drv_products_raw.json, drv_amazon_price.json
# output: drv_copurchase_selected.csv, drv_products_selected.json

import json
import numpy as np

products = json.load(open('data/drv_products_raw.json'))
price_dict = json.load(open('data/amazon_price.json'))

# selection criteria: we have the price in the dictionary 

selected_products = []
customer_dict = {} # record purchases of customers

product_idx = 0
for product in products:
	ASIN = product['ASIN']
	if ASIN not in price_dict or product['total_review'] < 5:
		continue

	price = price_dict[ASIN]
	
	customer_ids = product['customer_ids']

	sales_count = len(customer_ids) # may be different from total_review
	selected_products.append({'ASIN': ASIN, 'price':price, 'sales_count':sales_count})

	for customer_id in customer_ids:
		if customer_id not in customer_dict:
			customer_dict[customer_id] = [product_idx]
		else:
			customer_dict[customer_id].append(product_idx)

	product_idx += 1

N_product = len(selected_products)
print ('number of selected products:', N_product)

print ('number of customers:', len(customer_dict))

count = 0
for customer_id in customer_dict:
	if len(customer_dict[customer_id]) >= 1:
		count += 1

print ('constructing the co-purchase matrix...')
copurchase_mat = np.zeros(shape=(N_product, N_product))

for customer_id in customer_dict:
	if customer_id == 'ATVPDKIKX0DER': # this customer is abnormal
		continue
	products_purchased = customer_dict[customer_id]
	for product_i in products_purchased:
		for product_j in products_purchased:
			if product_j != product_i:
				copurchase_mat[product_i][product_j] += 1

with open('data/drv_products_selected.json', 'w') as output_file:
	json.dump(selected_products, output_file, indent=4)
np.savetxt('data/drv_copurchase_selected.csv', copurchase_mat, delimiter=',', fmt='%d')