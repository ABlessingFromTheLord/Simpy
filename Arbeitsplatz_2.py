import itertools

list1 = [1, 2, 3]
permuted = list(itertools.permutations([1, 2, 3]))
for i in range(len(permuted)):
    permuted[i] = list(permuted[i])

print(permuted)
print(sum(list1))
