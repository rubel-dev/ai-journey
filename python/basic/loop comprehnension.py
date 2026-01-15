
lst = [n*n for n in range(1, 20) if n%2 ==1]
print(lst)

names =["rubel", 'sakib', 'jannati']

names = [x.upper() for x in names]

print(names)

duplist = [2, 3, 4, 2, 3, 4]
new_lst = []
[new_lst.append(x) for x in duplist if x  not in new_lst]
print(new_lst)

dic = {n: n**3 for n in range(1, 20) if n%2 == 0}
print(dic)

s = "hello world"
freqs = {ch: s.count(ch) for ch in s }
print(freqs)