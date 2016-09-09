# Remove equal adjacent elements
#
# Example input: [1, 2, 2, 3]
# Example output: [1, 2, 3]
def remove_adjacent(lst):
	nlst = []
	if lst:
		nlst.append(lst[0])
	for i in range(1, len(lst)):
		if lst[i] != lst[i - 1]:			
			nlst.append(lst[i])
	return nlst
 
# Merge two sorted lists in one sorted list in linear time
#
# Example input: [2, 4, 6], [1, 3, 5]
# Example output: [1, 2, 3, 4, 5, 6]
def linear_merge(lst1, lst2):
	nlst = [] 
	while lst1 and lst2:
		if lst1[0] > lst2[0]:
			nlst.append(lst2.pop(0))
		else: 
			nlst.append(lst1.pop(0))
	nlst.extend(lst1)
	nlst.extend(lst2)
	return nlst