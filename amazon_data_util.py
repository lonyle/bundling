# modules to deal with the raw data


# from the input file, get one products
def read_a_product(input_file):
	product = {}
	line = input_file.readline()
	while not line.split(): #empty line
		line = input_file.readline()
		if not line: # empty product
			return None
	
	# skip till Id:
	while line.split()[0] != 'Id:':
		line = input_file.readline()
		while not line.split(): # empty line
			line = input_file.readline()			

	line = input_file.readline() # ASIN
	ASIN = line.split()[1]
	product['ASIN'] = ASIN

	line = input_file.readline() # title
	if line.split()[0] != 'title:':
		return -1

	line = input_file.readline() # group
	group = line.split()[1]
	product['group'] = group

	line = input_file.readline() # sales rank
	sales_rank = int(line.split()[1])
	product['sales_rank'] = sales_rank

	while line.split()[0] != 'reviews:':
		line = input_file.readline()
	total_review = int(line.split()[2])
	product['total_review'] = total_review

	line = input_file.readline()

	customer_ids = []
	# read the reviews
	while line != "\n":
		customer_id = line.split()[2]
		customer_ids.append(customer_id)
		line = input_file.readline()

	product['customer_ids'] = customer_ids
	return product

def get_products():
	input_filename = 'data/amazon-meta.txt'
	product_vec = []
	with open(input_filename, 'r') as input_file:
		product = read_a_product(input_file)
		while product != None:
			if product != -1:
				product_vec.append(product)
			product = read_a_product(input_file)
	return product_vec