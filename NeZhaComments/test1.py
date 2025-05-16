import happybase

def main():
    try:
        # 连接到 HBase
        connection = happybase.Connection(host='localhost', port=9090)
        print("Connected to HBase")

        # 获取 `test_table` 表
        table = connection.table('test_table')

        # 扫描表中的所有数据
        print("Scanning 'test_table' table:")
        for key, data in table.scan():
            print(f"Row key: {key.decode()}, Data: {data}")

        # 获取 `test_table` 表
        table = connection.table('test_table')

        # 扫描表中的所有数据
        print("Scanning 'test_table' table:")
        for key, data in table.scan():
            print(f"Row key: {key.decode()}, Data: {data}")

        # 关闭连接
        connection.close()
        print("Connection closed")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == '__main__':
    main()