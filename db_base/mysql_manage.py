#coding:utf-8


def createTable(table_class):
    table_class.create_table()


def dropTable(table_class):
    table_class.drop_table()


def reCreateTable(table_class):
    table_class.drop_table()
    table_class.create_table()

if __name__ == "__main__":
    pass
