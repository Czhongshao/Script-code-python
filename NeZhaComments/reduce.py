import sys
from collections import defaultdict

def reduce_function(user, counts):
    total_comments = sum(counts)
    print(f"{user}\t{total_comments}")

if __name__ == "__main__":
    current_user = None
    counts = []

    for line in sys.stdin:
        user, count = line.strip().split('\t')
        count = int(count)

        if user != current_user:
            if current_user:
                for key, value in reduce_function(current_user, counts):
                    print(f"{key}\t{value}")
            current_user = user
            counts = []

        counts.append(count)

    if current_user:
        for key, value in reduce_function(current_user, counts):
            print(f"{key}\t{value}")