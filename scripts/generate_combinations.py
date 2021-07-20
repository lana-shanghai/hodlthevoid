from itertools import product

amin = 0
amax = 6
combos = list(map(list,product(range(amin, amax), repeat=5)))

print(combos[0], combos[1233])

'''
with open('combos.txt', 'w') as f:
    for item in combos:
        f.write("%s\n" % item)
'''