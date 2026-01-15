
lst = [2, 4, 6, 2]
 
freq = {}
for x in lst:
     freq[x] = freq.get(x, 0) + 1


print(freq)

uniq_lst = list(set(lst))
print(uniq_lst)