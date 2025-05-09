import sys

def map_function():
    for line in sys.stdin:
        line = line.strip()
        parts = line.split('\t')
        if len(parts) == 5:
            _, _, rating, _, _ = parts
            print(f"{rating}\t1")

if __name__ == "__main__":
    map_function()