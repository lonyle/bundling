# input: amazon-meta.txt
# output: drv_products.json

import amazon_data_util
import json

products = amazon_data_util.get_products()

output_filename = 'data/drv_products_raw.json'
with open(output_filename, 'w') as output_file:
	json.dump(products, output_file, indent=4)