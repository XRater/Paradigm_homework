import sys, os
from hashlib import md5

def func(root_folder):
	d = {}
	for root, dirs, files in os.walk(root_folder):
		for f in files:
			if f[0] == '~' or f[0] == '.':
				continue;
			path = root + '\\' + f
			with open(path, "br") as newf:
				content = newf.read()
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
	func(root_folder)
	   	
if __name__ == '__main__':
	main()
        
