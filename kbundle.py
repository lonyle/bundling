# these are heuristic algorithms to solve the k-bundle problem

# input: mean vector \mu, covariance matrix Cov 
# output: the optimal k set

import sys
import pi
import random

import math
from cvxopt import matrix
from cvxopt import solvers
import numpy as np
import profit
import json

import matplotlib.pyplot as plt

# the aim is to 
#   1. select the problematic set of products
#   2. choose from these products so that the variance is minimized
def Kbundle_QP_relaxation(mu_vec, Cov_mat, alpha, K, separate_profit_vec):
	N = len(mu_vec)
	# M is the parameter for the number of candidates. When M is small, the remaining gap is more important and reducing the variance is more important when M is large.
	gap_vec = [None] * N

	for i in range(N):
		gap_vec[i] = (mu_vec[i] - separate_profit_vec[i])

	print ('sorting the profit gaps of the products...')
	sorted_indices = [i[0] for i in sorted(enumerate(gap_vec), key=lambda x:x[1], reverse=True)]
	max_profit = -math.inf
	max_bundle = None

	chunk = 20

	opt_profit_vec = []

	for M in range(K, min(3*K+1, N), max(2*K//chunk,1) ):
		print ('====considering the first', M, 'product with highest gap')
		opt_soln = Kbundle_candidate(sorted_indices[:M], Cov_mat, K)

		# inner sampling
		opt_profit = -math.inf
		opt_bundle = None
		sample_size = 5 # we do randomized rounding for 5 times and obtain the best
		for i in range(sample_size):
			bundle_set, bundle_vec = random_set(opt_soln, K)

			variance_bundle = profit.variance(bundle_vec, Cov_mat)
			variance_opt = profit.variance(opt_soln, Cov_mat)
			print (pi.bcolors.FAIL,'opt=', variance_opt, 'bundle=', variance_bundle  , pi.bcolors.ENDC)
			profit_ = profit.profit_bundle(bundle_set, bundle_vec, mu_vec, Cov_mat, alpha, separate_profit_vec)

			if profit_ > opt_profit:
				opt_profit = profit_
				opt_bundle = bundle_set

		print ('opt_profit:', opt_profit)
		opt_profit_vec.append(opt_profit)
		if opt_profit > max_profit:
			max_profit = opt_profit
			max_bundle = opt_bundle
	print ('opt_profit_vec:', opt_profit_vec)
	return max_bundle, max_profit

def Kbundle_candidate(candidate_list, Cov_mat, K):
	Cov_mat_sub = Cov_mat[:,candidate_list][candidate_list]

	total_product = Cov_mat.shape[0]
	# construct the quadratic programming
	N = len(candidate_list)

	P = matrix(Cov_mat_sub, tc='d')
	q = matrix(np.zeros([N, 1]), tc='d')
	# box constraints
	G_matrix = []
	for i in range(N):
		vec = [0] * N
		vec[i] = 1
		G_matrix.append(vec)
	for i in range(N):
		vec = [0] * N
		vec[i] = -1
		G_matrix.append(vec)
	G = matrix(np.array(G_matrix), tc='d')
	h_vec = [0] * 2 * N
	for i in range(N):
		h_vec[i] = 1
	h = matrix(np.array(h_vec), tc='d')

	# equality constraints
	A = matrix(np.array([[1]*N]), tc='d')
	b = matrix(np.array([K]), tc='d')
	# solve it
	solvers.options['maxiters'] = 200
	#solvers.options['show_progress'] = False
	result = solvers.qp(P, q, G, h, A, b)

	opt_soln_sub = result['x']
	obj_val = result['primal objective']
	opt_soln = [0] * total_product
	for i in range(N):
		candidate = candidate_list[i]
		opt_soln[candidate] = opt_soln_sub[i]

	return opt_soln

# generate random set proportional according to weight
def random_set(weight, K):	
	rounded_vec = dependent_rounding(weight, K)
	choices = []
	for i in range(len(rounded_vec)):
		if rounded_vec[i] == 1:
			choices.append(i)
	return set(choices), rounded_vec

def dependent_rounding(weight, K):
	# with open('data/tmp_weight_before_rounding_'+str(K)+'.json', 'w') as output_file:
	print ('dependent rounding')
	print ('sum of weight before rounding:', sum(weight))
	N = len(weight)
	indices = [i for i in range(N)]
	random.shuffle(indices)
	prob_vec = [None] * N
	rounded_vec = [None] * N
	for i in range(N):
		prob_vec[i] = weight[ indices[i] ]

	first = 0
	second = 1
	while (second < N):
		#print (indices[first], indices[second])
		beta1, beta2 = simplify(prob_vec[first], prob_vec[second])
		prob_vec[first] = beta1
		prob_vec[second] = beta2
		if (beta1 == 0 or beta1 == 1):
			rounded_vec[ indices[first] ] = beta1
			first = second
			second += 1
		elif (beta2 == 0 or beta2 == 1):
			rounded_vec[ indices[second] ] = beta2
			second += 1
		else:
			print ('error, no var fixed')
	rounded_vec[ indices[first] ] = prob_vec[first]
	print ('sum of rounded_vec', sum(rounded_vec))
	return list(map(lambda x:int(round(x)), rounded_vec))

def simplify(beta1, beta2):
	beta1 = min(1, beta1)
	beta2 = min(1, beta2)
	Pr1 = beta1
	Pr2 = beta2
	if beta1 + beta2 == 0:
		Pr1 = 0
		Pr2 = 0
	elif beta1 + beta2 <= 1:
		if random.random() < (beta2)/(beta1+beta2):
			Pr1 = 0
			Pr2 = beta1 + beta2
		else:
			Pr2 = 0
			Pr1 = beta1 + beta2
	elif beta1 + beta2 < 2:
		if random.random() < (1-beta2)/(2-beta1-beta2):
			Pr1 = 1
			Pr2 = min(1, beta1 + beta2 - 1)
		else:
			Pr2 = 1
			Pr1 = min(1, beta1 + beta2 - 1)
	elif beta1 + beta2 == 2:
		Pr1 = 1
		Pr2 = 1
	else:
		print ('error, total probability > 2', beta1 + beta2)

	return Pr1, Pr2