import sys, os
from hashlib import md5

def getfiles(root_folder):
	d = {}
	for root, dirs, files in os.walk(root_folder):
		for curr_file in files:
			path = root + '/' + curr_file
			path = os.path.normpath(path)
			if curr_file[0] == '~' or curr_file[0] == '.' or os.path.islink(path):
				continue;
			with open(path, "br") as f:
				content = f.read()
			m =  md5()
			m.update(content)
			key = m.hexdigest()
			if d.get(key, 0):
				d[key].append(path)
			else:
				d[key] = [path]
	return d;

def print_simular(d):
	for key, value in d.items():
		if len(value) > 1: 
			print(':'.join(value))
			

def main(): 
	if len(sys.argv) != 2:
		print('Wrong format')
		sys.exit()
	root_folder = sys.argv[1]
	d = getfiles(root_folder)
	print_simular(d)
	   	
if __name__ == '__main__':
	main()
        
