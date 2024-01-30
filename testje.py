from itertools import combinations

items1 = ['apple', 'banana', 'yoghurt', 'water', 'beer', 'computer']
items2 = ['grocery', 'bag', 'spoon', 'geo', 'pen']

all_items = items1 + items2

for r in range(2, 12):
    print(f'Combinations of length {r}:')
    for combo in combinations(all_items, r):
        print(list(combo))
