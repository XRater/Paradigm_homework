import numpy as np
import sys              
#a = np.array([2, 3, 4, 5])
#b = np.array([3, 4, 5, 6])
#a = np.vstack((a, b))
#print(a)

def get_matrix(input_file):
	matrix_both = np.loadtxt(input_file, dtype = int)
	n = matrix_both.shape[1]
	k = 1
	while k < n:
		k *=2 
	mat_a =  matrix_both[:n]
	mat_a = np.hstack( (mat_a,  np.zeros((n, k - n), dtype = int) ) )
	mat_a = np.vstack( (mat_a,  np.zeros((k - n, k), dtype = int) ))
	mat_b = matrix_both[n:]
	mat_b = np.hstack( (mat_b,  np.zeros((n, k - n), dtype = int)) )
	mat_b = np.vstack( (mat_b,  np.zeros((k - n, k), dtype = int)) )   
	return(mat_a, mat_b, k, n)

def mult_matrix(mat_a, mat_b, n):
	if n == 1:
		return mat_a*mat_b
	else:
		n = n//2;
		a11 = mat_a[:n, :n]
		a12 = mat_a[:n, n:]
		a21 = mat_a[n:, :n]
		a22 = mat_a[n:, n:] 
		b11 = mat_b[:n, :n]
		b12 = mat_b[:n, n:]
		b21 = mat_b[n:, :n]
		b22 = mat_b[n:, n:]

		mat_1 = mult_matrix(a11 + a22, b11 + b22, n)
		mat_2 = mult_matrix(a21 + a22, b11, n)
		mat_3 = mult_matrix(a11, b12 - b22, n)
		mat_4 = mult_matrix(a22, b21 - b11, n)
		mat_5 = mult_matrix(a11 + a12, b22, n)
		mat_6 = mult_matrix(a21 - a11, b11 + b12, n)
		mat_7 = mult_matrix(a12 - a22, b21 + b22, n)
						
		c11 = mat_1 + mat_4 - mat_5 + mat_7
		c21 = mat_2 + mat_4
		c12 = mat_3 + mat_5
		c22 = mat_1 + mat_3 - mat_2 + mat_6

		c_top = np.hstack((c11, c12))
		c_bottom = np.hstack((c21, c22))
		c = np.vstack((c_top, c_bottom))
		return c

def print_matrix(matrix, size):
	
	for row in matrix[:size, :size]:
		print(' '.join(map(str, row)))

def main(): 
	if len(sys.argv) != 2:
		print('Wrong format')
		sys.exit()
	input_file = sys.argv[1]
	mat_a, mat_b, n, real_size = get_matrix(input_file)
	mat_c = mult_matrix(mat_a, mat_b, n)	
	print_matrix(mat_c, real_size)
	

if __name__ == '__main__':
	main()	  

