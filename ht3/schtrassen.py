import numpy as np

def get_matrix(n):	
	arr = []
	for i in range (n):
		arr.append(input().split())
	mat_a = np.matrix(arr, dtype = int)	  
	return mat_a                         

def resize_matrix(mat_a, size):
	n = mat_a.shape[0]
	if (size > n):
		mat_a = np.hstack((mat_a,  np.zeros((n, szie - n), dtype = mat_a.dtype)))
		mat_a = np.vstack((mat_a,  np.zeros((size - n, size), dtype = mat_a.dtype)))  
		return mat_a
	else: 
		mat_a = mat_a[:size, :size]
		return mat_a

def mult_matrix(mat_a, mat_b):	
	if mat_a.shape[0] == 1:
		return mat_a*mat_b
	else:
		n = mat_a.shape[0] // 2
		a11 = mat_a[:n, :n]
		a12 = mat_a[:n, n:]
		a21 = mat_a[n:, :n]
		a22 = mat_a[n:, n:] 
		b11 = mat_b[:n, :n]
		b12 = mat_b[:n, n:]
		b21 = mat_b[n:, :n]
		b22 = mat_b[n:, n:]
		mat_1 = mult_matrix(a11 + a22, b11 + b22)
		mat_2 = mult_matrix(a21 + a22, b11)
		mat_3 = mult_matrix(a11, b12 - b22)
		mat_4 = mult_matrix(a22, b21 - b11)
		mat_5 = mult_matrix(a11 + a12, b22)
		mat_6 = mult_matrix(a21 - a11, b11 + b12)
		mat_7 = mult_matrix(a12 - a22, b21 + b22)						
		c11 = mat_1 + mat_4 - mat_5 + mat_7
		c21 = mat_2 + mat_4
		c12 = mat_3 + mat_5
		c22 = mat_1 + mat_3 - mat_2 + mat_6
		c = np.zeros((mat_a.shape[0], mat_a.shape[0]), dtype = mat_a.dtype) 
		c[:n, :n] = c11
		c[:n, n:] = c12
		c[n:, :n] = c21
		c[n:, n:] = c22
		return c

def print_matrix(matrix):
	for row in matrix:
		print(' '.join(map(str, row)))     

def main(): 
	real_size = int(input())
	mat_a = get_matrix(real_size)
	mat_b = get_matrix(real_size)
	size = 1
	while size < real_size:
		size *= 2 
	mat_a = resize_matrix(mat_a, size)
	mat_b = resize_matrix(mat_b, size)
	mat_c = mult_matrix(mat_a, mat_b)
	mat_c = resize_matrix(mat_c, real_size)	
	print_matrix(mat_c)
	

if __name__ == '__main__':
	main()	  

