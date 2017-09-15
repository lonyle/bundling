# pre-processing
echo "1. retrieving the products from amazon-meta.txt..."
python n01_products_raw.py 
echo "2. filtering the products and constructing the co-purchaing matrix..."
python n02_products_copurchase_select.py

# learning (inferrence)
echo "3. calculating the co-purchasing probability..."
python n03_copurchase_prob.py
echo "4. inferring the mean and standard deviation of valuations..."
python n04_empirical_mean_std.py 
echo "5. calculation the empirical correlation coefficients..."
python n05_empirical_cor.py 
echo "6. symmetric matrix factorization..."
python n06_smf.py 20 #20 is the number of factors
echo "7. measuring the accuracy of inferred parameters..."
python n07_accuracy.py 20

# running algorithms
echo "8. running our bundling algorithm on the Amazon dataset..."
python n08_run_kbundle.py 
echo "9. calculating the approximation ratio with 20 randomly chosen products..."
python n09_approximation_ratio.py
