def most_frequent(nums):
	return max(set(nums), key = nums.count)

listers = [1,2,3,4,5,5,55,6,7,8,5,2,5,8,9,41,3,5,87]

print(most_frequent(listers))

print("testing")