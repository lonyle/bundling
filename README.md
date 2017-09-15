# Download the data file
	Due to storage issue, I did NOT put the data file into this repository. 
	Please download from https://snap.stanford.edu/data/bigdata/amazon/amazon-meta.txt.gz
	Then upzip it, put in the 'data/' folder as 'data/amazon_meta.txt'.

# Prerequisite
	Some python packages need to be installed, including numpy, pandas, scipy, multiprocessing and cvxopt.

# How to run
	$ bash manifest.sh

# Files 
	├── amazon_data_util.py					some util files
	├── baseline_random.py					random select k products to bundle
	├── data 								
	│   ├── amazon-meta.txt					Amazon product co-purchasing dataset (from SNAP, Stanford)
	│   └── amazon_price.json				prices of some products on Amazon (crawled from thetracktor.com)
	├── determine_f.py					determine the parameter a in f(.)
	├── exp_setting.py					bundle size settings
	├── kbundle.py						Our bundling algorithm (Algorithm 3)
	├── manifest.sh						!!! run all the experiments
	├── n01_products_raw.py					
	├── n02_products_copurchase_select.py
	├── n03_copurchase_prob.py
	├── n04_empirical_mean_std.py
	├── n05_empirical_cor.py
	├── n06_smf.py
	├── n07_accuracy.py
	├── n08_run_kbundle.py
	├── n09_approximation_ratio.py
	├── pi.py						$\pi(.)$ function
	├── profit.py						calculate the profit of a bundling strategy
	└── README
