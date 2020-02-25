import openpyxl


def main():

    table_list = []
    #with open("TargetTables.txt", 'r', encoding='UTF8') as fr:
    with open("TableList.txt", 'r', encoding='UTF8') as fr:
        for r_line in fr:
            table_list.append(r_line.strip())
    print(len(table_list))
    print(table_list)

    # 엑셀파일 열기
    excel_file = openpyxl.load_workbook('Input.xlsx')

    excel_sheet1 = excel_file['Sheet1']

    excel_sheet2 = excel_file['Sheet2']

    primary_keys = {}
    no_primary_keys = [] #pk 없는 테이블 리스트 확인용
    fw = open("Create.sql", 'w', encoding='UTF8')


    for line in excel_sheet2.rows:
        t_key = line[0].value
        if t_key in table_list:
            primary_keys[t_key] = primary_keys.get(t_key, []) + [line[1].value]
    # q = {}
    # for line2 in excel_sheet1.rows:
    #     t_key = line2[0].value
    #     if t_key in table_list:
    #         q[t_key] = q.get(t_key,[]) + [line2[1].value + line2[2].value]
    ex_tables = []  # 테이블리스트에는 있고 엑셀에는 없는 테이블을 닮을 리스트
    for line2 in excel_sheet1.rows:
        t_key = line2[0].value
        ex_tables.append(t_key)  # 엘셀에있는테이블 리스트
        if t_key in table_list:
            pKey = ''
            outline = line2[1].value + line2[2].value + '\n'

            if t_key in primary_keys:
                pKey = ','.join(primary_keys[t_key])
                pKey = pKey.upper()
            # else:  # Sheet2에 없는 key 값 저장
            #     no_primary_keys.append(t_key)

            if 'CREATE' in outline:  # 첫째 줄
                loc = outline.find('CREATE')
                outline = outline[loc:]
                outline = outline.replace('(','(\n',1)

            if ');' in outline:  # 마지막 줄
                if outline.find('ETL_DEL_YN CHAR(1),') != -1:
                    outline = outline.replace('ETL_DEL_YN CHAR(1),', 'ETL_DEL_YN CHAR(1) DEFAULT \'N\' NOT NULL, ')
                if outline.find('ETL_LOAD_DT DATETIME') != -1:
                    if len(pKey) != 0:
                        outline = outline.replace('ETL_LOAD_DT DATETIME);',
                                                  'ETL_LOAD_DT DATETIME DEFAULT CURRENT TIMESTAMP NOT NULL, ')
                        outline = outline + 'PRIMARY KEY(' + pKey + ',ETL_DEL_YN,ETL_LOAD_DT)\n);'
                    else:
                        no_primary_keys.append(t_key)# Sheet2에 없는 key 값 저장
                        outline = outline.replace('ETL_LOAD_DT DATETIME);',
                                                  'ETL_LOAD_DT DATETIME DEFAULT CURRENT TIMESTAMP NOT NULL\n);')

                    # if t_key in primary_keys:
                    #     pKey = ','.join(primary_keys[t_key])
                    #     pKey = pKey.upper()
                    # else: #Sheet2에 없는 key 값 저장
                    #     no_primary_keys.append(t_key)
                    # if len(pKey) != 0:
                    #     outline = outline + 'PRIMARY KEY(' + pKey + ',ETL_DEL_YN,ETL_LOAD_DT);\n);'
                    # else:
                    #     outline = outline + ');'
                outline = outline.replace(', ', ',\n') # 컴마뒤에 개행 추가
                outline = outline + '\n'
            #print(outline)
            fw.write(outline)

    # print('before q : {}'.format(q))
    # for value in q.values():
    #     loc = value[0].find('CREATE')
    #     value[0] = value[0][loc:]
    #     value[0].replace('(','(\n',1)
    #
    #     last = value[-1]
    #     d = ' ,'
    #     m = last.split(d)
    #
    # print(m)
    # print('last : {}'.format(last))
    # print('after q : {}'.format(q))
    # print("value: {}".format(value))
    fw.close()
    excel_file.close()

    no_tables = []
    for t_name in table_list:
        if t_name not in ex_tables:
            no_tables.append(t_name)

    print(primary_keys)
    print(len(primary_keys))
    print('no PK tables : {}'.format(no_primary_keys))
    print('no Exel tables : {}'.format(no_tables))



if __name__ == "__main__":
    main()


