import sys

def map_function(row_key, row_data):
    # 提取用户名称
    user = row_data.get('cf:comment_user', None)
    if user:
        # 输出键值对 (用户名称, 1)
        print(f"{user}\t1")

if __name__ == "__main__":
    for line in sys.stdin:
        parts = line.strip().split('\t')
        if len(parts) >= 5:
            row_key = parts[0]
            row_data = {
                'cf:comment_user': parts[1],
                'cf:rating': parts[2],
                'cf:comment_time': parts[3],
                'cf:comment': parts[4]
            }
            for key, value in map_function(row_key, row_data):
                print(f"{key}\t{value}")