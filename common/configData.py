import os
import readConfig as readConfig
from xlrd import open_workbook
from xml.etree import ElementTree as ElementTree
import json

proDir = readConfig.proDir


# ****************************** read testCase from excel ********************************
def get_xls(xls_name, sheet_name):
    cls = []
    # get xls file's path
    xlsPath = os.path.join(proDir, "testFile", 'case', xls_name)

    # open xls file
    file = open_workbook(xlsPath)

    # get sheet by name
    sheet = file.sheet_by_name(sheet_name)
    # 获取表格行数
    nrows = sheet.nrows
    # 获取表格列数
    # ncols = sheet.ncols
    for i in range(nrows):
        if sheet.row_values(i)[0] != u'case_name':
            # 获取整行的值存入数组
            cls.append(sheet.row_values(i))

    return cls


def get_params_xls(xls_name, sheet_name):
    pls = []
    # get xls file's path
    xlsPath = os.path.join(proDir, "testFile", 'case', xls_name)

    # open xls file
    file = open_workbook(xlsPath)

    # get sheet by name
    sheet = file.sheet_by_name(sheet_name)
    # 获取表格行数
    nrows = sheet.nrows
    # 获取表格列数
    # ncols = sheet.ncols
    for i in range(nrows):
        if sheet.row_values(i)[0] == u'case_name':
            # 获取整行的值存入数组
            pls = sheet.row_values(i)

    return pls


# ****************************** read SQL xml ********************************
database = {}


def set_xml():
    if len(database) == 0:
        sql_path = os.path.join(proDir, "testFile\case", "SQL.xml")
        tree = ElementTree.parse(sql_path)
        for db in tree.findall("database"):
            db_name = db.get("name")
            # print(db_name)
            table = {}
            for tb in db.getchildren():
                table_name = tb.get("name")
                # print(table_name)
                sql = {}
                for data in tb.getchildren():
                    sql_id = data.get("id")
                    # print(sql_id)
                    sql[sql_id] = data.text
                table[table_name] = sql
            database[db_name] = table


def get_xml_dict(database_name, table_name):
    set_xml()
    database_dict = database.get(database_name).get(table_name)
    return database_dict


def get_sql(database_name, table_name, sql_id):
    db = get_xml_dict(database_name, table_name)
    sql = db.get(sql_id)
    return sql


def get_json(response, key):
    """
    获取返回值指定key的value
    :param response:
    :param key:
    :return:
    """
    return_json = response.json()
    json_value = return_json[key]
    return json_value

    # ****************************** read interfaceURL xml ********************************


def get_url_from_xml(name):
    url_list = []
    url_path = os.path.join(proDir, 'testFile', 'interfaceURL.xml')
    tree = ElementTree.parse(url_path)
    for u in tree.findall('url'):
        url_name = u.get('name')
        if url_name == name:
            for child in u.getchildren():
                url_list.append(child.text)

    url = '/'.join(url_list)
    return url


def show_return_msg(response):
    """
    show msg detail
    :param response:
    :return:
    """
    # url = response.url
    msg = response.text
    # print("\n请求地址：" + url)
    # 可以显示中文
    print("\n请求返回值：" + '\n' + json.dumps(json.loads(msg), ensure_ascii=False, sort_keys=True, indent=4))


def get_value_from_return_json(json, name1, name2):
    """
    get value by key
    :param json:
    :param name1:
    :param name2:
    :return:
    """
    info = json['info']
    group = info[name1]
    value = group[name2]
    return value


# if __name__ == "__main__":
#     # abc = get_xls('userCase.xlsx', 'login')
#     # for aa in abc:
#     #     print(aa)
#
#     par = get_params_xls('userCase.xlsx', 'login')
#
#     for b in par:
#         print(b)
