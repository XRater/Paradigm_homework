import sys, os
from hashlib import md5

def getfiles(root_folder):
	d = {}
	for root, _, files in os.walk(root_folder):
		for curr_file in files:           
			path = os.path.join(root, curr_file)
			if curr_file[0] == '~' or curr_file[0] == '.' or os.path.islink(path):
				continue
			key = get_hash(path)
			d[key] = d.get(key, [])
			d[key].append(path)
	print(d)
	return d

def get_hash(path):
	m =  md5()
	with open(path, "br") as f:
		inf = f.read(1024)
		while inf:
			m.update(inf)
			inf = f.read()
	return m.hexdigest()

def print_simular(d):
	for value in d.values():
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
        
