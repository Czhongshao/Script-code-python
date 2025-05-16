import happybase

def main():
    connection = happybase.Connection(host='localhost', port=9090)
    print("Connected to HBase")
    
    # 创建表
    try:
        connection.create_table('test_table', {'cf': dict()})
        print("Table 'test_table' created")
    except Exception as e:
        print("Table might already exist:", e)
    
    table = connection.table('test_table')

    # 插入数据
    table.put(b'row1', {'cf:col1': 'value1', 'cf:col2': 'value2'})
    table.put(b'row2', {'cf:col1': 'value3', 'cf:col2': 'value4'})
    print("Data inserted")
    
    # 查询数据
    print("Row1 data:", table.row('row1'))
    for key, data in table.scan():
        print(f"Row key: {key}, Data: {data}")

    # # 删除数据
    # table.delete('row1', columns=['cf:col1'])
    # print("Column 'cf:col1' in 'row1' deleted")

    # # 删除表
    # connection.disable_table('test_table')
    # connection.delete_table('test_table')
    # print("Table 'test_table' deleted")

    # 关闭连接
    connection.close()
    print("Connection closed")

if __name__ == '__main__':
    main()
