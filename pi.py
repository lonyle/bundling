# solving the maximization problem of profit

from scipy import optimize
from scipy.stats import norm
import math

def pi(mu, sigma_square, alpha, c):
	params = mu, sigma_square, c
	ranges = slice(0.01, 0.99, 0.01)
	resbrute = optimize.brute(f_exponential, (ranges,), args = params, full_output = True, finish = optimize.fmin)
	return (resbrute[0], -resbrute[1]) # 0: global minimum argmax, 1: max

def f_exponential(delta, *params):
	mu, sigma_square, c = params
	# exponential weight
	return -((norm.ppf(1-delta) * math.sqrt(math.fabs(sigma_square)) + mu) - c) * mapping(delta)

def mapping(delta):
	a = 16674.27	
	return 	(a**delta - 1)/(a - 1) # multiplied by 1/f(1) and don't change the PftImp

# for printing
class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'