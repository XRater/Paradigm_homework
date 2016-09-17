import sys, os
from hashlib import md5

def finddoubles(root_folder):
	d = {}
	for root, dirs, files in os.walk(root_folder):
		for curr_file in files:
			if curr_file[0] == '~' or curr_file[0] == '.':
				continue;
			path = root + '\\' + curr_file
			with open(path, "br") as f:
				content = f.read()
			m =  md5()
			m.update(content)
			key = m.hexdigest()
			if d.get(key, 0):
				d[key].append(path)
			else:
				d[key] = [path]

	for key, value in d.items():
		if len(value) > 1:
			print(value.pop(), end = '')
			for f in value:
				print(':'+ f, end = '')
			print()            



def main(): 
	if len(sys.argv) != 2:
		print('Wrong format')
		sys.exit()
	root_folder = sys.argv[1]
	finddoubles(root_folder)
	   	
if __name__ == '__main__':
	main()
        
