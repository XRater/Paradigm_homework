import numpy as np

def get_matrix(n):	
	arr = []
	for i in range (n):
		arr.append(input().split())
	mat_a = np.array(arr, dtype = int)
	return(mat_a)                         

def resize_matrix(mat_a, n):
	k = 1
	while k < n:
		k *= 2 
	mat_a = np.hstack((mat_a,  np.zeros((n, k - n), dtype = int)))
	mat_a = np.vstack((mat_a,  np.zeros((k - n, k), dtype = int)))  
	return (mat_a, k)

def mult_matrix(mat_a, mat_b, n):	
	if n == 1:
		return mat_a*mat_b
	else:
		n = n // 2
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

		c = np.zeros((2 * n, 2 * n), dtype = int) 
		c[:n, :n] = c11
		c[:n, n:] = c12
		c[n:, :n] = c21
		c[n:, n:] = c22
		return c

def print_matrix(matrix, size):

	for row in matrix[:size, :size]:
		print(' '.join(map(str, row)))     

def main(): 
	real_size = int(input())
	mat_a = get_matrix(real_size)
	mat_b = get_matrix(real_size)
	mat_a, size = resize_matrix(mat_a, real_size)
	mat_b, size = resize_matrix(mat_b, real_size)
	mat_c = mult_matrix(mat_a, mat_b, size)	
	print_matrix(mat_c, real_size)
	

if __name__ == '__main__':
	main()	  

