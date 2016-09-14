import sys, os

def func(root_folder):
	for root, dirs, files in os.walk(root_folder):
		print(root, "consumes", end=" ")
		for f in files:
			print(root + '/' + f, end = ', ')
		print()
	#	print(sum(getsize(join(root, name)) for name in files), end=" ")
	#	print("bytes in", len(files), "non-directory files")


def main(): 
	if len(sys.argv) != 2:
		print('Wrong format')
		sys.exit()
	root_folder = sys.argv[1]
	func(root_folder)
	   	
if __name__ == '__main__':
	main()