# Remove equal adjacent elements
#
# Example input: [1, 2, 2, 3]
# Example output: [1, 2, 3]
def remove_adjacent(lst):
	nlst = []
	for i in iter(lst):              
		if (lst(i) != nex):
			nst.append(nexlst(i))
	return nlst
 
# Merge two sorted lists in one sorted list in linear time
#
# Example input: [2, 4, 6], [1, 3, 5]
# Example output: [1, 2, 3, 4, 5, 6]
def linear_merge(lst1, lst2):
	nlst = []
	i = 0
	j = 0
	while((i < len(lst1)) or (j < len(lst2))):
		if (i == len(lst1)):
			nlst.append(lst2[j])
			j += 1
		elif (j == len(lst2)):
			nlst.append(lst1[i])
			i += 1
		elif (lst1[i] < lst2[j]):
			nlst.append(lst1[i])
			i += 1
		else:
			nlst.append(lst2[j])
			j+=1	
	return nlst
                                   
