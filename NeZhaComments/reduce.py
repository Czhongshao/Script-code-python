import sys
from collections import defaultdict

def reduce_function():
    count_dict = defaultdict(int)
    for line in sys.stdin:
        line = line.strip()
        rating, count = line.split('\t')
        count_dict[rating] += int(count)
    
    for rating, count in count_dict.items():
        print(f"{rating}\t{count}")

if __name__ == "__main__":
    reduce_function()